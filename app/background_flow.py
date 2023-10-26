import openai
import os

from dotenv import load_dotenv
from pipeline.flows.agi import Consciousness
from pipeline.config.config import config
from pipeline.shared_content import logger
from pipeline.shared_content import agents
from pipeline.functions.LlamaAsyncInterface import LlamaAsyncInterface


load_dotenv()
config.ai["provider"] = os.getenv("LLM_PROVIDER")
config.open_ai_key = os.getenv("API_KEY", "")
config.model = os.getenv("OPENAI_MODEL", "gpt-4")
config.ai["model"] = config.model

if config.ai["provider"] == 'openai':
    openai.api_key = config.open_ai_key
    config.ai["ai"] = openai
elif config.ai["provider"] == 'llama2':
    ai_server = os.getenv("LLAMA_ADDRESS")
    config.ai["ai"] = LlamaAsyncInterface(ai_server=ai_server)
    
from pipeline.agent.agi import agent_simulation, agent_thought_factory, agent_gate_keepr, agent_dm

logger.info("set shared content")
agents["GATE_KEEPER"] = agent_gate_keepr
agents["THOUGHT_FACTORY"] = agent_thought_factory
agents["SIMULATION"] = agent_simulation
agents["DM"] = agent_dm

logger.info("set background flow")
flow = Consciousness(config, agents=agents, api="OPENAI", observation=None)
