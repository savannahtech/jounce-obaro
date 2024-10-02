from metric_simulator.lib.base import LLMBase, LLMMetrics


class OpenAILLM(LLMBase):
    def __init__(self, name, **kwargs):
        """
        Initializes the OpenAILLM class with the given name and sets up the environment.
        """
        # Call the parent class constructor to initialize ranges
        super().__init__()

        self.llm_name = name

    def get_ttft(self):
        """
        Generates data points for the Time to First Token (TTFT) metric.
        """
        return self.get_data_points(LLMMetrics.TIME_TO_FIRST_TOKEN.value)

    def get_tps(self):
        """
        Generates data points for the Tokens Per Second (TPS) metric.
        """
        return self.get_data_points(LLMMetrics.TOKENS_PER_SECOND.value)

    def get_e2e_latency(self):
        """
        Generates data points for the End-to-End Latency (E2E Latency) metric.
        """
        return self.get_data_points(LLMMetrics.END_TO_END_LATENCY.value)

    def get_rps(self):
        """
        Generates data points for the Requests Per Second (RPS) metric.
        """
        return self.get_data_points(LLMMetrics.REQUESTS_PER_SECOND.value)
