from typing import Literal
from base_config.logger.logger import logger
from app.client_management.tavily_client import tavily_client_management
from api.monitor.monitor import monitor

tavily_client_management.init()
client = tavily_client_management.client


def internet_search(
        query:str,
        search_depth:Literal["basic", "advanced", "fast", "ultra-fast"],
        time_range:Literal["day", "week", "month", "year"],
        topic:str="general",
        max_results:int=3,
        timeout:float=30.0,
):
    """
    根据用户问题进行互联网内容搜索
    :param query: 需搜索的问题
    :param search_depth: 搜索方式:"basic", "advanced", "fast", "ultra-fast" -- 分别对应普通搜索，前沿搜索，快速搜索，超快搜索
    :param topic："general"
    :param time_range:搜索内容时间跨度："day", "week", "month", "year -- 分别对应每日，每周，每月，每年
    :param max_results: 最大搜索内容结果数量，设定为3
    :param timeout: 超时设定为30
    :return: 搜索的内容结果，工具报错时，返回报错内容
    """
    monitor.report_tool("Tavily互联网搜索:internet_search")
    try:
        result = client.search(
            query=query,
            search_depth=search_depth,
            topic=topic,
            time_range=time_range,
            max_results=max_results,
            timeout=timeout
        )
        logger.info(f"tavily生成答案:{result}")
        return result
    except Exception as e:
        logger.error(str(e))
        return str(e)

if __name__ == "__main__":
    a = internet_search("什么是电商直播","basic","week")
    print(a)











