from langchain.chat_models import init_chat_model
from base_config.config.config import config as conf

llm = init_chat_model(
    model=conf.llm.model,
    base_url=conf.llm.url,
    api_key=conf.llm.api_key,
    model_provider=conf.llm.model_provider
)


ollama_llm = init_chat_model(
    model="qwen3.5:9b",
    model_provider="ollama",
)


from langchain_ollama import ChatOllama

ollama_llm_m = ChatOllama(model="qwen3.5:9b")



if __name__ == "__main__":
    #result = ollama_llm.invoke("你好")
    #print(result)
    ming = ollama_llm_m.invoke("你好")
    print(ming)



