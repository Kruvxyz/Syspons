from pipeline.agent.agent import Agent
from pipeline.config.config import config
from dotenv import load_dotenv
import os
import openai

load_dotenv()
openai.api_key = os.getenv("API_KEY", config.open_ai_key)

ai_config = {
    "ai": openai, "provider": 'openai', "model": "gpt-3.5-turbo"
}

system_prompt = """You are an helpful assistant, complete every task you are given."""

magic_assistant = Agent("helpful_assistant",
                        ai=ai_config, system_prompt=system_prompt, commands=[])
