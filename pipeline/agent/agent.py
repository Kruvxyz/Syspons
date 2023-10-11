from typing import Any, Callable, Dict, List, Optional, Tuple
from pipeline.functions import count_tokens
from pipeline.config.config import config
from pipeline.shared_content import logger

class Agent:
  def __init__(self,
               name: str,
               ai: Any,
               commands: List["Command"],
               system_prompt: str,
               prompt_generator: Optional[Callable[[Dict[str, str]], str]] = None,
               answer_max_tokens: Optional[int] = None
    ) -> None:
    logger.info(f"Agent:{name}: Initiate")
    self.name = name
    self.ai = ai
    self.commands = commands
    self.system_prompt = system_prompt
    self.prompt_generator = prompt_generator
    self.answer_max_tokens = answer_max_tokens
    self.history = []
    logger.info(f"Agent:{self.name}: Initiate done")

  def get_expected_converation_tokens(self) -> int:
    #fixme(guyhod): for this project we don't have memory, when memory will be added it should be part of calculation
    return count_tokens(self.system_prompt) + (
        self.answer_max_tokens if self.answer_max_tokens else 0
    )

  def talk(self, user_input: str, user_data: Optional[Dict[str, str]] = None, answer_max_tokens: Optional[int] = None) -> str:
    logger.info(f"Agent:{self.name}: talk")
    if self.prompt_generator and user_data:
        user_input = self.prompt_generator(user_data)

    logger.info(f"Agent:{self.name}: talk-this: {user_input}")
    if answer_max_tokens or self.answer_max_tokens:
        max_tokens = self.answer_max_tokens if self.answer_max_tokens else 0
        max_tokens = answer_max_tokens if answer_max_tokens else max_tokens
        resp = self.ai.ChatCompletion.create(
          model=config.model,
          messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_input},
            ],
          max_tokens=max_tokens
        )

    else:
      resp = self.ai.ChatCompletion.create(
        model=config.model,
        messages=[
              {"role": "system", "content": self.system_prompt},
              {"role": "user", "content": user_input},
          ]
      )
    logger.info(f"Agent:{self.name}: talk-response: {str(resp)}")
    return resp["choices"][0]["message"]["content"]

  def push_message(self, message: Dict[str, str]) -> None:
      logger.info(f"Agent:{self.name}: push_message: {str(message)}")
      self.history.append(message)

  def reset(self):
      logger.info(f"Agent:{self.name}: reset")
      self.history = []

  def train(self, *args, **kwargs) -> None:
      # TODO(guyhod): future / empty interface for now
      pass
  
  def get_system_prompt(self) -> str:
     return self.system_prompt
  
  def set_system_prompt(self, system_prompt: str) -> None:
     self.system_prompt = system_prompt
