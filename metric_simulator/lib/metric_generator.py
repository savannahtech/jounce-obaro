from metric_simulator.lib import ClaudeLLM, LLamaLLM, LLMType
from metric_simulator.lib.openai.index import OpenAILLM


class MetricGeneratorFactory:
    @staticmethod
    def get_llm(llm_type: LLMType, name: str, **kwargs):
        """
        Instantiates and returns the appropriate Language Learning Model (LLM) based on the specified LLM type.

        Args:
            llm_type (LLMType): The type of language model to use.
            name (str): The name of the LLM instance.
            **kwargs: Additional keyword arguments for initializing the specific LLM.

        Returns:
            OpenAILLM, LLamaLLM, or ClaudeLLM: An instance of the selected LLM based on the LLM type.

        Raises:
            ValueError: If the specified LLM type is unknown.
        """
        if llm_type == LLMType.OPENAI.value:
            return OpenAILLM(name, **kwargs)
        elif llm_type == LLMType.LLAMA.value:
            return LLamaLLM(name, **kwargs)
        elif llm_type == LLMType.CLAUDE.value:
            return ClaudeLLM(name, **kwargs)
        else:
            raise ValueError("Unknown llm type")


class MetricGenerator:
    def __init__(self, llm_type: LLMType, name: str, **kwargs):
        self.llm = MetricGeneratorFactory.get_llm(llm_type, name, **kwargs)

    def generate_data_points(self, metric: str):
        """
        Generates data points for a given metric using the underlying Language Learning Model (LLM).
        Validates the metric name and raises an error if it is not recognized.

        Args:
            metric (str): The metric for which to generate data points.

        Returns:
            list: A list of data points for the specified metric.

        Raises:
            ValueError: If the specified metric is unknown.
        """
        # Mapping of metric names to methods
        metric_methods = {
            "ttft": self.llm.get_ttft,
            "tps": self.llm.get_tps,
            "e2e_latency": self.llm.get_e2e_latency,
            "rps": self.llm.get_rps,
        }
        if metric not in metric_methods:
            raise ValueError(f"Unknown metric: {metric}")

        metric_values = metric_methods[metric]()
        return metric_values
