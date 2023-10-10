import openai
import os

from dotenv import load_dotenv
from pipeline.flows.agi import Consciousness
from pipeline.config.config import config
from pipeline.shared_content import logger


load_dotenv()
config.open_ai_key = os.getenv("API_KEY", "")
config.model = os.getenv("OPENAI_MODEL", "gpt-4")

openai.api_key = config.open_ai_key
config.ai = openai
from pipeline.agent.agi.simulation import agent_simulation
from pipeline.agent.agi.thought import agent_thought
from pipeline.agent.agi.mind import agent_mind

logger.info("set background flow")
flow = Consciousness(config, agents={"MIND": agent_mind, "THINK": agent_thought,
                     "SIMULATION": agent_simulation}, api="OPENAI", observation=None)
