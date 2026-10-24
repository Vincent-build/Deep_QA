from langchain.tools import tool
import json
from base_config.logger.logger import logger
from app.client_management.ragflow_client import ragflow_client_management
from api.monitor.monitor import monitor

ragflow_client_management.init()
client = ragflow_client_management.client

@tool
def get_assistant_list():
    """
    获取聊天助手列表
    :return: 返回聊天助手信息，工具报错时返回报错信息
    """
    monitor.report_tool("获取助手列表:get_assistant_list")
    try:
        response = client.list_chats()
        assistant_list = [{"助手名称":f"{ans.name}","功能介绍":ans.description,"关联知识库":ans.kb_names} for ans in response]
        return assistant_list
    except Exception as e:
        logger.error(str(e))
        return str(e)




@tool
def create_ask_delete(chat_name,query):
    """
    创建会话session，通过询问助手，获取相关的答案内容
    注意：调用此工具之前，必须先调用get_assistant_list，明确可用助手名称和助手能力边界
    :param chat_name: 助手名称，必须通过get_assistant_list工具获取该助手名称
    :param query: 用户问题
    :return: 返回用户问题的答案，工具报错时返回报错内容
    """
    monitor.report_tool("使用会话助手:create_ask_delete",args={"会话助手名称":chat_name})
    try:
        chats = client.list_chats(name=chat_name)
        if chats:
            session = chats[0].create_session("deepagent_session")
            response = session.post(
                path=f"/chats/{chats[0].id}/completions",
                json={
                    "messages":[{"role":"user","content":query}],
                    "stream":True,
                    "session_id":session.id
                }
            )

            response_mes = ""
            for res in response.iter_lines(decode_unicode=True):
                if not res:
                    continue
                message = res.removeprefix("data:").strip()
                line = json.loads(message)
                if not isinstance(line["data"],dict):
                    continue
                data = line.get("data")
                answer = data.get("answer")
                if answer.startswith(response_mes):
                    response_mes = answer
                elif not response_mes.startswith(answer):
                    response_mes += answer

            chats[0].delete_sessions(ids=[session.id])

            monitor.report_tool("会话助手反馈消息",{"text":response_mes})
            return response_mes
        else:
            return "不存在会话助手"

    except Exception as e:
        logger.error(str(e))
        return str(e)









