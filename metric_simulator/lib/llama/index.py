from metric_simulator.lib.base import LLMBase, LLMMetrics


class LLamaLLM(LLMBase):
    def __init__(self, name, **kwargs):
        """
        Initializes the LLamaLLM class with the given name and environment variables.
        """
        # Call the parent class constructor to initialize ranges
        super().__init__()

        self.llm_name = name

    def get_ttft(self):
        """
        Retrieves data points for Time To First Token (TTFT) metric.
        """
        return self.get_data_points(LLMMetrics.TIME_TO_FIRST_TOKEN.value)

    def get_tps(self):
        """
        Retrieves data points for Tokens Per Second (TPS) metric.
        """
        return self.get_data_points(LLMMetrics.TOKENS_PER_SECOND.value)

    def get_e2e_latency(self):
        """
        Retrieves data points for End-To-End Latency metric.
        """
        return self.get_data_points(LLMMetrics.END_TO_END_LATENCY.value)

    def get_rps(self):
        """
        Retrieves data points for Requests Per Second (RPS) metric.
        """
        return self.get_data_points(LLMMetrics.REQUESTS_PER_SECOND.value)
