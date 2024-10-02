import os
from typing import Any

import redis
from dotenv import load_dotenv

from database import LLMRepository, MetricRepository, SimulatorRepository
from logger import logging
from metric_simulator.lib import MetricGenerator
from metric_simulator.utils import retry_on_failure
from redis_client import RedisClient, RedisKeys

load_dotenv()

MAX_RETRIES = int(os.getenv("MAX_RETRIES", "2"))
RETRY_DELAY = int(os.getenv("RETRY_DELAY", "60"))


class MetricService:
    """
    This class provides methods to simulate data points and remove metrics.
    """

    def __init__(
        self,
        llm_repository: LLMRepository,
        metric_repository: MetricRepository,
        simulator_repository: SimulatorRepository,
    ):
        """
        Initializes the MetricService with the provided repositories.
        """
        self.llm_repository = llm_repository
        self.metric_repository = metric_repository
        self.simulator_repository = simulator_repository

    @retry_on_failure(
        redis_client=RedisClient(), max_retries=MAX_RETRIES, delay=RETRY_DELAY
    )
    async def generate_metric_data(
        self, metric_generator: Any, metric_name: str, llm_name: str
    ):
        generated_metrics = metric_generator.generate_data_points(metric_name)
        return generated_metrics

    async def simulate_data_points_with_retry(self):
        redis_client = RedisClient()
        try:
            with redis_client.redis.lock(
                RedisKeys.RETRY_BENCHMARKS_LOCK.value,
                timeout=MAX_RETRIES * RETRY_DELAY,
                blocking=True,
                blocking_timeout=10,
            ) as lock:
                await self.simulate_data_points()
        except redis.exceptions.LockError as lock_error:
            logging.error(f"Redis lock error: {lock_error}")
        except Exception as e:
            logging.error(f"Error during simulating data points: {e}")
        finally:
            # Check if the lock exists and locked before trying to release
            if "lock" in locals() and lock.locked():
                try:
                    lock.release()
                except redis.exceptions.LockError:
                    logging.info("Lock was already released")

    async def simulate_data_points(self):
        """
        Simulates data points for all LLMs and metrics.
        It uses MetricGenerator to generate the data points and stores them with SimulatorRepository
        """
        llms = self.llm_repository.get_llms()
        metrics = self.metric_repository.get_metrics()

        # remove existing data points
        self.remove_metrics()
        redis_client = RedisClient()
        for llm in llms:
            metric_generator = MetricGenerator(llm.company_name, llm.name)
            for metric in metrics:
                generated_metrics = await self.generate_metric_data(
                    metric_generator, metric.name, llm.name
                )
                if generated_metrics:
                    self.simulator_repository.bulk_add_metrics(
                        llm.id, metric.id, generated_metrics
                    )
                    redis_client.redis.delete(
                        f"{RedisKeys.RETRY_BENCHMARKS.value}:{llm.id}:{metric.id}"
                    )
                    if redis_client.redis.exists(
                        f"{RedisKeys.METRIC_BENCHMARKS.value}:{metric.name}"
                    ):
                        redis_client.delete_key(
                            f"{RedisKeys.METRIC_BENCHMARKS.value}:{metric.name}"
                        )

        if redis_client.redis.exists(RedisKeys.BENCHMARKS.value):
            redis_client.delete_key(RedisKeys.BENCHMARKS.value)

    def remove_metrics(self):
        """
        Removes all metrics from the database.
        """
        self.simulator_repository.remove_all_metrics()
