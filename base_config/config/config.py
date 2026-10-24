from omegaconf import OmegaConf
from dataclasses import dataclass
from pathlib import Path

@dataclass
class MySQLConfig:
    user: str
    password: str
    host: str
    port: str
    charset: str
    collection: str
    sql_mode: str
    database: str
    table1: str
    table2: str
    table3: str


@dataclass
class RAGFlowConfig:
    api_key: str
    url: str


@dataclass
class TavilyConfig:
    api_key: str


@dataclass
class LLMConfig:
    url: str
    api_key: str
    model: str
    model_provider: str


@dataclass
class AppConfig:
    mysql:MySQLConfig
    ragflow:RAGFlowConfig
    tavily:TavilyConfig
    llm:LLMConfig

path_ = Path(__file__).parents[0] / "config.yaml"

structured = OmegaConf.structured(AppConfig)

schema = OmegaConf.load(path_)

merged = OmegaConf.merge(structured,schema)

config:AppConfig = OmegaConf.to_object(merged)

if __name__ == "__main__":
    print(config.llm.model)







