import os
from typing import Any, Callable, Dict, List, Optional, Tuple

model_to_tokens = {
    # DO NOT CHANGE! ORDER IS IMPORTANT, FOR ANY CHANGE VERIFY THAT get_tokens_for_model(model) WORKS CORRECTLY!
    # https://platform.openai.com/docs/models/gpt-4
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-16k": 16385,
    "gpt-4": 8192,
    "gpt-4-32k": 32768,
    "text-davinci-002": 4097,
    "code-davinci-002": 8001,
    "babbage-002": 16384,
    "davinci-002": 16384
}


def get_tokens_for_model(model: str) -> int:
    tokens = 0
    for m in model_to_tokens:
        if m in model:
            tokens = model_to_tokens[m]
    return tokens


class Config:
    """
    Configuration class to store consts.
    """

    def __init__(self) -> None:
        """Initialize the Config class"""
        self.open_ai_key = ""
        self.model = "gpt-4"
        self.max_tokens = get_tokens_for_model(self.model)
        self.file_names = ["temporary.txt"]  # should be overwrite
        self.output_file_name = "output.txt"  # should be overwrite
        self.ai = None
        
        # States
        self.STATE_RUN = 'RUN'
        self.STATE_CONTINUE = 'CONTINUE'
        self.STATE_NONE = 'NONE'

        # Commands
        # fixme(guyhod): refactor commands as objects which passes to flow/agent and contain full functionality
        self.COMMAND_END_FLOW = "END_OF_FLOW"
        self.COMMAND_FLAG = "FLAG"
        self.COMMAND_SUMMARY = "SUMMARY"
        self.COMMAND_STORE = "STORE"
        self.COMMAND_STORE_AND_END_FLOW = "STORE_AND_END_FLOW"
        self.COMMAND_ANSWER = "ANSWER"

    def set_filenames(self, file_names: List[str]) -> None:
        self.file_names = file_names

    def set_output_filename(self, file_name) -> None:
        self.output_file_name = file_name


config = Config()
