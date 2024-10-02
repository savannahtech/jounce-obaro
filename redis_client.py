import os
from enum import Enum

import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "")
REDIS_PORT = os.getenv("REDIS_PORT", "")


class RedisKeys(Enum):
    BENCHMARKS = "benchmarks"
    METRIC_BENCHMARKS = "benchmarks_metric"
    RETRY_BENCHMARKS = "retry_benchmarks"
    RETRY_BENCHMARKS_LOCK = "retry_benchmarks_lock"


class RedisClient:
    """
    A client for interacting with a Redis database.
    """

    def __init__(self):
        """
        Initializes a new instance of the RedisClient class.
        Connects to a Redis server.
        """
        self.redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

    def delete_key(self, key: str):
        """
        Deletes a key from the Redis database if it exists and has a value.

        Args:
            key (str): The key to delete from the Redis database.

        Returns:
            None
        """
        if self.redis.exists(key):
            value = self.redis.get(key)
            if value:
                self.redis.delete(key)
