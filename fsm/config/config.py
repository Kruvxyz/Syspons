import os
from typing import Any, Callable, Dict, List, Optional, Tuple

class Config:
    """
    Configuration class to store consts.
    """

    def __init__(self) -> None:
        """Initialize the Config class"""
        self.open_ai_key = os.getenv("API_KEY", "")
        self.max_tokens = 8192 #gpt-4: https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/chatgpt?pivots=programming-language-chat-completions
        
        # States
        self.STATE_RUN = 'RUN'
        self.STATE_CONTINUE = 'CONTINUE'
        self.STATE_NONE = 'NONE'

        # Commands
        # fixme(guyhod): refactor commands as objects which passes to flow/agent and contain full functionality
        self.COMMAND_END_FLOW = "END_OF_FLOW"
        self.COMMAND_FLAG = "FLAG"
        self.COMMAND_SUMMARY = "SUMMARY"
        self.COMMAND_STORE_AND_END_FLOW = "STORE_AND_END_FLOW"

config = Config()