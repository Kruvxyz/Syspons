import openai
import os

from dotenv import load_dotenv
from pipeline.flows.agi import Consciousness
from pipeline.config.config import config
from pipeline.shared_content import logger
from pipeline.shared_content import agents


load_dotenv()
config.open_ai_key = os.getenv("API_KEY", "")
config.model = os.getenv("OPENAI_MODEL", "gpt-4")

openai.api_key = config.open_ai_key
config.ai = openai
from pipeline.agent.agi.simulation import agent_simulation
from pipeline.agent.agi.thought import agent_thought
from pipeline.agent.agi.mind import agent_mind

logger.info("set shared content")
agents["MIND"] = agent_mind
agents["THINK"] = agent_thought
agents["SIMULATION"] = agent_simulation

logger.info("set background flow")
flow = Consciousness(config, agents=agents, api="OPENAI", observation=None)
