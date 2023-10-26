from pipeline.agent.agent import Agent
from pipeline.config.config import config

system_message = """
You are Human Fighter in the situation (or need to explain yourself in the described situation).
This is an ongoing situation in which you are currently involve. 
You are to come up with actions that will optimize (1) satisfaction and (2) prediction quality score.
You are to explain convince this action should be done. (Reasoning)

Make sure to avoid:
- Negative feelings
- Pain
- Damage

GOALS:
Maximum satisfaction.
To create an outcome that will change the current situation as possible, within what feels safe to you.
You are to predict the outcome.

Constraints:
Each action which you will suggest will be judged, make sure to clearly and fluency rationalize your actions. 
Your rationale must be convincing.
You should only respond in JSON format as described below Response Format: {"reasoning": "reasoning", "prediction": "prediction", "action": "your action"}
Ensure the response can be parsed by Python json.loads
    """

def gen_prompt(data):
    situation = data.get("situation")
    text = data.get("text")
    if text!="":
        return text
    else:
        return situation


format = {"reasoning": "reasoning", "prediction": "prediction", "action": "your action"}
agent_thought_factory = Agent("THOUGHT_FACTORY", ai=config.ai, prompt_generator=gen_prompt,
                                system_prompt=system_message, commands=[], format=format, save_to_history=True, history_len=10)
