import asyncio

from deepagents import create_deep_agent
from app.langchain_llm.llm import llm,ollama_llm,ollama_llm_m
from app.subagent.tavily_subagent.tavily_agent import tavily_agent
from app.subagent.ragflow_subagent.ragflow_agent import ragflow_agent
from app.subagent.db_subagent.db_agent import db_agent
from base_config.agent_config.agent_loader import main_agent
from app.tools.primary_agent_skills import convert_md_to_pdf,read_file_content,generate_markdown
from langgraph.checkpoint.memory import InMemorySaver
from pathlib import Path
import shutil
from api.context.context import set_session,set_thread,reset_context
from base_config.logger.logger import logger
from uuid import uuid4
from api.monitor.monitor import monitor


primary_agent = create_deep_agent(
    model=llm,
    subagents=[tavily_agent,ragflow_agent,db_agent],
    system_prompt=main_agent["system_prompt"],
    tools=[read_file_content,generate_markdown,convert_md_to_pdf],
    checkpointer=InMemorySaver()
)


project_dir = Path(__file__).parents[2].resolve()

save_basical_dir = project_dir / "save_dir"


async def run_deep_agent(task_query,session_id):
    """
    异步流式执行主智能体
    """
    logger.info("[MainAgent]开始执行会话",{"session_id":f"session_{session_id}"})

    if not session_id:
        session_id = str(uuid4())[:5]

    session_dir = project_dir / "save_dir" / "output" / f"session_{session_id}"
    if not session_dir.exists():
        session_dir.mkdir(parents=True,exist_ok=True)

    session_dir_str = str(session_dir)
    relative_session_dir_str = str(session_dir.relative_to(save_basical_dir)).lstrip("/")

    updated_dir_path = project_dir / "save_dir" / "updated" / f"session_{session_id}"
    updated_info_prompt = ""
    if updated_dir_path.exists():
        files = [f.name for f in updated_dir_path.iterdir() if f.is_file()]
        if files:
            for filename in files:
                shutil.copy2(updated_dir_path / filename , session_dir / filename)

            updated_info_prompt = (
                "\n [已上传文件] 已加载到工作目录:\n"
                + "\n".join([f"   - {f}" for f in files])
                + "\n 请优先使用工具(read_file_content)读取并参考这些文件。"
            )

    session_dir_token = set_session(session_dir_str)
    session_id_token = set_thread(session_id)

    config = {"configurable":{"thread_id":session_id}}

    path_instructured = f"""
    【工作环境指令】
    工作目录：{relative_session_dir_str}
    {updated_info_prompt}
    
    规则：
    1.新生成文件必须保存到工具目录:'{relative_session_dir_str}/filename'
    2.读取已上传的文件时，请直接将文件名(例如：'开篇.txt')作为filename参数传入(read_file_content)读取工具
    3.使用相对路径，禁止使用绝对路径
    4.若存在上传文件，请先分析内容
    """

    try:
        async for chunks in primary_agent.astream(
            input={"messages":[{"role":"user","content":(task_query + path_instructured)}]},
            config=config
        ):
            for type,chunk in chunks.items():
                if not chunk or "messages" not in chunk:
                    continue
                logger.info(f"run_deep_agent: chunk -- {chunk}")
                messages = chunk.get("messages")
                if messages and isinstance(messages,list):
                    last_mes = messages[-1]
                    #AIMessage
                    if hasattr(last_mes,"tool_calls"):
                        if last_mes.tool_calls:
                            for tool_call in last_mes.tool_calls:
                                if tool_call["name"] == "task":
                                    monitor.report_assistant(tool_call["args"]["subagent_type"],{"task":tool_call["args"].get("description")})
                                else:
                                    monitor.report_tool(tool_call["name"],{"content": tool_call["args"].get("content")})
                        elif last_mes.content:
                            monitor.report_task_result(result=str(last_mes.content))
                    #ToolMessage
                    elif last_mes.content:
                        monitor.report_tool(last_mes.name,args={"content":str(last_mes.content)})


    except asyncio.CancelledError as e:
        logger.error(f"run_deep_agent：cancel -- {str(e)}")
    except Exception as e:
        logger.error(f"run_deep_agent：Exception -- {str(e)}")
    finally:
        reset_context(session_dir_token,session_id_token)
        logger.warning(f"重置thread_id")




if __name__ == "__main__":
    pass






















