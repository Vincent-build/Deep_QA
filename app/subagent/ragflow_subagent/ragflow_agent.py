from base_config.agent_config.agent_loader import ragflow_subagent
from app.tools.ragflow_skills import get_assistant_list,create_ask_delete


ragflow_agent = {
    "name":ragflow_subagent["name"],
    "description":ragflow_subagent["description"],
    "system_prompt":ragflow_subagent["system_prompt"],
    "tools":[get_assistant_list,create_ask_delete]
}





















