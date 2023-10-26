import time
from typing import Any, Callable, Dict, List, Optional, Tuple

import openai
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
               answer_max_tokens: Optional[int] = None,
               format: Dict[str, str]={},
               save_to_history: bool = False,
               history_len: int = 0
    ) -> None:
    logger.info(f"Agent:{name}: Initiate")
    self.name = name
    self.ai_provider = ai.get("provider", "openai")
    self.ai_model = ai.get("model", config.model)
    self.ai = ai["ai"]
    self.commands = commands
    self.system_prompt = system_prompt
    self.prompt_generator = prompt_generator
    self.answer_max_tokens = answer_max_tokens
    self.history = []
    self.response_format = format
    self.save_to_history = save_to_history
    self.history_len = history_len
    logger.info(f"Agent:{self.name}: Initiate done")

  def llm(self, agent_prompt, answer_max_tokens:int = None, history_len: int = None) -> str:
    """
    Connect to LLM and return response as string
    """
    history = []
    if history_len is None:
       history_len = self.history_len

    if history_len > 0: #fixme(guyhod): should consider token limitation
       if len(self.history) > history_len:
          history = self.history[len(self.history) - history_len:]
       else:
         history = self.history

    if self.ai_provider=="openai":
      messages=[
                  {"role": "system", "content": self.system_prompt},
                  *history,
                  {"role": "user", "content": agent_prompt},
              ]

      if answer_max_tokens or self.answer_max_tokens:
          max_tokens = self.answer_max_tokens if self.answer_max_tokens else 0
          max_tokens = answer_max_tokens if answer_max_tokens else max_tokens
          resp = self.ai.ChatCompletion.create(
            model=self.ai_model,
            messages=messages,
            max_tokens=max_tokens
          )

      else:
        resp = self.ai.ChatCompletion.create(
          model=self.ai_model,
          messages=messages
        )
      logger.info(f"Agent:{self.name}: talk-response: {str(resp)}")
      return resp["choices"][0]["message"]["content"]
    
    elif self.ai_provider=="llama2":
      resp = self.ai.query(system_prompt=self.system_prompt, agent_prompt=agent_prompt, history=history)
      generated_text = resp['answer'][0]['generated_text']
      print(f"resp: {str(resp)}")
      print(f"text: {generated_text[generated_text.find('[/INST]')+8:]}")
      logger.info(f"Agent:{self.name}: talk-response: {str(resp)}")
      return generated_text[generated_text.find("[/INST]")+8:]

    else:
       raise ValueError("ai provider must be openai or llama2")
        
     
  def get_expected_converation_tokens(self) -> int:
    #fixme(guyhod): for this project we don't have memory, when memory will be added it should be part of calculation
    return count_tokens(self.system_prompt) + (
        self.answer_max_tokens if self.answer_max_tokens else 0
    )

  def prepare_agent_prompt(self, user_input: str, user_data: Optional[Dict[str, str]] = None) -> str:
    if self.prompt_generator and user_data:
      user_input = self.prompt_generator(user_data)
    return user_input
  
  def talk(self, user_input: str, user_data: Optional[Dict[str, str]] = None, answer_max_tokens: Optional[int] = None, history_len: int = None) -> str:
    # fixme: user_data seems redundent amd user_input should named user_prompt
    logger.info(f"Agent:{self.name}: talk")
    # user_prompt = self.prepare_agent_prompt(user_input, user_data)
    user_prompt = user_input

    logger.info(f"Agent:{self.name}: talk-this: {user_prompt}")
    for i in range(3):
      try:
        agent_response = self.llm(agent_prompt=user_prompt, answer_max_tokens=answer_max_tokens, history_len=history_len)
        break
      except Exception as e:
        if i==2:
          raise e
        logger.warning(f"Agent:{self.name} - attemp {i} fail to query LLM")
        time.sleep(30)
        
    if self.save_to_history:
       self.push_message({
        "role": "user",
        "content": user_prompt
        })
       
       self.push_message({
        "role": "assistant",
        "content": agent_response
        })
    return agent_response

  def push_message(self, message: Dict[str, str]) -> None:
      logger.info(f"Agent:{self.name} | message: {str(message)}")
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
