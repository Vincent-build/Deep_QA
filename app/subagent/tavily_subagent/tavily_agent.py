from app.tools.tavily_skills import internet_search
from base_config.agent_config.agent_loader import tavily_subagent



tavily_agent = {
    "name":tavily_subagent["name"],
    "description":tavily_subagent["description"],
    "system_prompt":tavily_subagent["system_prompt"],
    "tools":[internet_search]
}






