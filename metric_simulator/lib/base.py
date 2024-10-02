from abc import ABC, abstractmethod
from enum import Enum

from metric_simulator.utils import generate_data_points


class LLMType(Enum):
    """
    Enum for defining types of Language Learning Models (LLMs).
    """

    OPENAI = "openai"
    LLAMA = "meta"
    CLAUDE = "anthropic"


class LLMMetrics(Enum):
    """
    Enum for defining metrics related to Language Learning Models (LLMs).
    """

    TIME_TO_FIRST_TOKEN = "ttft"
    TOKENS_PER_SECOND = "tps"
    END_TO_END_LATENCY = "e2e_latency"
    REQUESTS_PER_SECOND = "rps"


class LLMBase(ABC):
    """
    Abstract base class for Language Learning Models (LLMs).
    """

    def __init__(self):
        """
        Initializes the base class with predefined ranges for LLM metrics.
        """
        self.ranges = {
            "ttft": (0.05, 2.0),  # Time to First Token (seconds)
            "tps": (10, 150),  # Tokens Per Second
            "e2e_latency": (0.2, 10.0),  # End-to-End Request Latency (seconds)
            "rps": (1, 100),  # Requests Per Second
        }

    def get_data_points(self, metric: str):
        """
        Generates data points for a given metric within predefined ranges.

        Args:
            metric (str): The metric for which to generate data points.

        Returns:
            list: A list of data points for the specified metric.
        """
        ranges = self.ranges[metric]
        data_points = generate_data_points(ranges[0], ranges[1], self.llm_name, metric)
        return data_points

    @abstractmethod
    def get_ttft(self):
        """
        Abstract method to get data points for Time to First Token metric.
        """
        pass

    @abstractmethod
    def get_tps(self):
        """
        Abstract method to get data points for Tokens Per Second metric.
        """
        pass

    @abstractmethod
    def get_e2e_latency(self):
        """
        Abstract method to get data points for End-to-End Latency metric.
        """
        pass

    @abstractmethod
    def get_rps(self):
        """
        Abstract method to get data points for Requests Per Second metric.
        """
        pass
