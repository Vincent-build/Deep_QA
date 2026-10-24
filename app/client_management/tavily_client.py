from tavily import TavilyClient
from base_config.config.config import config as conf

class TavilyClientManaged:
    def __init__(self,api_key:str=conf.tavily.api_key):
        self.api_key = api_key
        self.client = None

    def init(self):
        self.client = TavilyClient(self.api_key)

    def close(self):
        self.client.close()

tavily_client_management = TavilyClientManaged()

if __name__ == "__main__":
    pass

