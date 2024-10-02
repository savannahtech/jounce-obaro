import asyncio
import hashlib
import os

import numpy as np
from dotenv import load_dotenv

from logger import logging
from redis_client import RedisKeys

load_dotenv()

SEED_VALUE = os.getenv("SEED", "")


def retry_on_failure(redis_client, max_retries=5, delay=60):
    def decorator(func):
        async def wrapper(metric_generator, metric_name, llm_name, *args, **kwargs):
            retry_key = f"{RedisKeys.RETRY_BENCHMARKS.value}:{llm_name}:{metric_name}"
            current_attempt = redis_client.redis.get(retry_key)
            if current_attempt is None:
                current_attempt = 0
            else:
                current_attempt = int(current_attempt)

            while current_attempt <= max_retries:
                try:
                    return await func(
                        metric_generator, metric_name, llm_name, *args, **kwargs
                    )
                except Exception as e:
                    redis_client.redis.set(
                        retry_key, current_attempt + 1, ex=60
                    )  # Set expiry for 60 seconds
                    logging.error(
                        f"Error generating metrics for LLM {llm_name}, attempt {current_attempt + 1}: {str(e)}"
                    )
                    current_attempt += 1
                    if current_attempt <= max_retries:
                        # wait before retrying
                        await asyncio.sleep(delay)

            logging.info(
                f"Max retries reached for LLM {llm_name} for metric {metric_name}, skipping."
            )
            return None

        return wrapper

    return decorator


def generate_data_points(
    min_val: float, max_val: float, llm_name: str, metric: str, size: int = 1000
) -> list:
    """
    Generates a list of random data points within a specified range.

    This function generates a specified number of random data points between a minimum and maximum value,
    rounded to two decimal places.

    Args:
        min_val (float): The minimum value of the range.
        max_val (float): The maximum value of the range.
        size (int, optional): The number of data points to generate. Defaults to 1000.

    Returns:
        list: A list of generated data points.
    """
    if SEED_VALUE:
        unique_string = f"{llm_name}_{metric}_{SEED_VALUE}"
        unique_seed = int(hashlib.md5(unique_string.encode()).hexdigest(), 16) % (2**32)
        np.random.seed(unique_seed)

    return np.round(np.random.uniform(min_val, max_val, size), 2).tolist()
