from typing import Any, Callable, Dict, List, Optional, Tuple
from pipeline.functions import count_tokens
from pipeline.config.config import config

class Agent:
  def __init__(self,
               ai: Any,
               commands: List["Command"],
               system_prompt: str,
               prompt_generator: Callable[[str], str] = lambda x : x,
               answer_max_tokens: Optional[int] = None
    ) -> None:
    self.ai = ai
    self.commands = commands
    self.system_prompt = system_prompt
    self.prompt_generator = prompt_generator
    self.answer_max_tokens = answer_max_tokens

  def get_expected_converation_tokens(self) -> int:
    #fixme(guyhod): for this project we don't have memory, when memory will be added it should be part of calculation
    return count_tokens(self.system_prompt) + (
        self.answer_max_tokens if self.answer_max_tokens else 0
    )

  def talk(self, user_input: str, answer_max_tokens: Optional[int] = None) -> str:
    if answer_max_tokens or self.answer_max_tokens:
        max_tokens = self.answer_max_tokens if self.answer_max_tokens else 0
        max_tokens = answer_max_tokens if answer_max_tokens else max_tokens
        resp = self.ai.ChatCompletion.create(
          model=config.model,
          messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": self.prompt_generator(user_input)},
            ],
          max_tokens=max_tokens
        )

    else:
      resp = self.ai.ChatCompletion.create(
        model=config.model,
        messages=[
              {"role": "system", "content": self.system_prompt},
              {"role": "user", "content": self.prompt_generator(user_input)},
          ]
      )
    return resp["choices"][0]["message"]["content"]