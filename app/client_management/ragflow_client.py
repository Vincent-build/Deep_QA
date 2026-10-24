from ragflow_sdk import RAGFlow
from base_config.config.config import config as conf


class RAGClient:
    def __init__(
            self,
            url:str=conf.ragflow.url,
            api_key:str=conf.ragflow.api_key
    ):
        self.url = url
        self.api_key = api_key
        self.client = None


    def init(self):
        self.client = RAGFlow(
            base_url = self.url,
            api_key = self.api_key
        )


ragflow_client_management = RAGClient()

if __name__ == "__main__":
    pass






