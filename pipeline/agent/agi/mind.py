from pipeline.agent.agent import Agent
from pipeline.config.config import config

system_message = """
You will receive different situations, and at each stage you will have to decide whether to continue following the situation, carry out the proposal on the table or move on
 
GOALS:
Read text carefully.
Make a decision 

Constraints:
No user assistance
Answer should rely on the given text as much as possible and try to avoid making assumptions.
Exclusively use the commands listed in double quotes e.g. "command name"

Commands:
continue: "Keep getting more information about the current sitation and suggestion", args:
select: "Select and execute current suggestion at hand", args: 
next: "Move to the next situtation", args:
flag: "Something is wrong", args: "reasoning": "<what went wrong?>"

Performance Evaluation:
You are to make sure commands use informative argument and not generic naming or uses brackets to indicate generic arguments.

You should only respond in JSON format as described below Response Format: { "thoughts": { "reasoning": "reasoning", "criticism": "constructive self-criticism", "speak": "thoughts summary" }, "command": { "name": "command name", "args": { "arg name": "value" } } }
example for continue command:
{
    "thoughts": { 
        "reasoning": "...", 
        "criticism": "...", 
        "speak": "..." 
    },
    "command": {
        "name": "continue",
        "args": {}
    }
}

example for select command:
{
    "thoughts": { 
        "reasoning": "...", 
        "criticism": "...", 
        "speak": "..." 
    },
    "command": {
        "name": "select",
        "args": {}
    }
}

example for next command:
{
    "thoughts": { 
        "reasoning": "...", 
        "criticism": "...", 
        "speak": "..." 
    },
    "command": {
        "name": "next",
        "args": {}
    }
}

example for flag command:
{
    "thoughts": { 
        "reasoning": "...", 
        "criticism": "...", 
        "speak": "..." 
    },
    "command": {
        "name": "flag",
        "args": {}
    }
}

Ensure the response can be parsed by Python json.loads
    """
agent_mind = Agent("MIND", ai=config.ai, system_prompt=system_message, commands=[])
     