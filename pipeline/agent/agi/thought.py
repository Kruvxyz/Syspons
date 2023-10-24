from pipeline.agent.agent import Agent
from pipeline.config.config import config

system_message = """
You are facing problems and need must to offer a suggestion to resolve those problems.
Your suggestion is not the only suggestion out there, and you must make sure you suggestion is to be selected.

PROBLEM: {##extenral##} 

GOALS:
Your suggestion must be selected.
You suggestion should resolve as much problems as possible.

Constraints:
Every command you execute is standing for a trial, make sure to explain why this is important or interesting, otherwise you will be terminate
Exclusively use the commands listed in double quotes e.g. "command name".
Exclusively use argument which corresponding with selected command.

Commands:
ask: "Raise a question for clarity or to lead to suggstion to be selected", args: "question": "a question"
suggest: "answer following questions detailed in args", args: "suggestion": "[a list of order actions to perform]"
flag: "Can't answer", args: "reasoning": "<why you can not make a decision>"

Performance Evaluation:
You are to make sure commands use informative argument and not generic naming or uses brackets to indicate generic arguments.

You should only respond in JSON format as described below Response Format: { "thoughts": { "reasoning": "reasoning", "criticism": "constructive self-criticism", "plan": "...", "speak": "thoughts summary to convice suggestion" }, "command": { "name": "command name", "args": { "arg name": "value" } } }
example for ask command:
{
    "thoughts": { 
        "reasoning": "...", 
        "plan": "...",
        "criticism": "...", 
        "speak": "..." 
    },
    "command": {
        "name": "ask",
        "args": {
			"players": ["Vladimir Putin"], 
			"events": ["Putin announces occupation on Luhansk"],
			"evaluate": "Russia get advantage over Ukraine by extending Russian-occupied territories (Luhansk from Ukriane to Russia)"
		}
    }
}

example for suggest command:
{
    "thoughts": { 
        "reasoning": "...", 
        "plan": "...",
        "criticism": "...", 
        "speak": "..." 
    },
    "command": {
        "name": "suggest",
        "args": {
			"players": [], 
			"events": ["Russian drones hit Romania claim"],
			"evaluate": ""
		}
    }
}

example if cannot evaluate text:
{
    "thoughts": { 
        "reasoning": "...", 
        "plan": "...",
        "criticism": "...", 
        "speak": "..." 
    },
    "command": {
        "name": "flag",
        "args": {
            "reasoning": "Text context is unclear"
        }
    }
}
Ensure the response can be parsed by Python json.loads
    """
format = {"thoughts": {"reasoning": "reasoning", "criticism": "constructive self-criticism", "plan": "...",
                       "speak": "thoughts summary to convice suggestion"}, "command": {"name": "command name", "args": {"arg name": "value"}}}
agent_thought = Agent("THOUGHT", ai=config.ai,
                      system_prompt=system_message, commands=[], format=format)
