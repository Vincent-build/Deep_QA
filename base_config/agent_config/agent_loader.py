import yaml
from pathlib import Path



path_ = str(Path(__file__).parents[0] / "prompt.yaml")

def load_agent(path):
    with open(path,"r") as f:
        template = yaml.safe_load(f)
    return template

template = load_agent(path_)

main_agent = template["main_agent"]

tavily_subagent = template["sub_agents"]["tavily"]

db_subagent = template["sub_agents"]["db"]

ragflow_subagent = template["sub_agents"]["ragflow"]









