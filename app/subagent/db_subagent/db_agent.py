from base_config.agent_config.agent_loader import db_subagent
from app.tools.db_skills import list_sql_tables,get_table_data,execute_sql_query


db_agent = {
    "name":db_subagent["name"],
    "description":db_subagent["description"],
    "system_prompt":db_subagent["system_prompt"],
    "tools":[list_sql_tables,get_table_data,execute_sql_query]
}














