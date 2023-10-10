from typing import Any, Callable, Dict, List, Optional, Tuple
from pipeline.functions import ParseResponse
from pipeline.shared_content import logger
import os.path as path

class AbstractFlow:
  def __init__(self, config: "Config") -> None:
    """
    Define agents here
    """
    self.config = config
    self.file_name: str = "output.txt"
    self.agents: Dict[str, "Agent"] = {}
    self.current_agent: Optional["Agent"] = None
    self.input: Any = ""  # input to propagate between states
    self.mem: str = "" # memory
    self.state: str = self.config.STATE_NONE
    self.agent_dict = {}

  def set_agent_dict(self) -> None:
    self.agent_dict = {self.agents[name]: name for name in self.agents}
    logger.info(f"flow: set_agent_dict: {str(self.agent_dict)}")

  def get_current_agent_state(self) -> str:
    current_agent_state = self.agent_dict.get(self.current_agent, None)  
    assert type(current_agent_state) != type(None), "Current agent state is not defined"
    return current_agent_state

  # def get_max_num_of_tokens(self) -> int:
  #   """
  #   Return maximum possible token per chunk
  #   Should consider internal / external intercace
  #   Calculation is somthing like:
  #   return max_tokens - max([agent.get_expected_converation_tokens() for agent in self.agents])
  #   """
  #   return 0
  
  def run(self, content: str = "") -> Optional[str]:
    """Execute FSM

    Args:
      content (str): flow initial text

    Returns:
      TBD
    """
    logger.info("flow: run")
    self.pre_execute_loop(content)
    logger.info("flow: run pre_execute_loop complete")

    while self.state == self.config.STATE_RUN:
      logger.info("flow: state: STATE_RUN")
      if type(self.input) is str:
        raw_answer = self.current_agent.talk(self.input)
      elif type(self.input) is dict: 
        raw_answer = self.current_agent.talk("", self.input)
      else:
        raise TypeError("flow->input type must be str or dict")

      logger.info(f"flow: raw_answer: {raw_answer}")
      answer = ParseResponse(raw_answer)
      command_name, args = self.parse_command(answer)
      command = command_name.upper()
      print(f"------------------{self.agent_dict[self.current_agent]}--------------------")
      print(f"thoughts: {answer.get('thoughts')}")
      print(f"command: {command}")
      print(f"args: {str(args)}")
      print("--------------------------------------")
      self.execute(answer)
    return None

  def pre_execute_loop(self, content: str) -> None:
    """Update self params befor executing loop

    Args:
      content (str): flow initial text

    Returns:
        None
    """
    self.state = self.config.STATE_RUN
    self.input = content

  def parse_command(self, data: Dict[str,Any]) -> Tuple[str, Dict[str, str]]:
    """Parse AI answer in Json format and return command and args

    Args:
      data (json): AI answer formatted as Json

    Returns:
        Command (str): Next action
        Args Dict[str, str]: argument with key values and values

    """
    command_dict = data.get("command")
    assert "name" in command_dict
    return command_dict["name"], command_dict.get("args", {})

  def execute(self, data: Dict[str,Any]) -> None:
    """Execute command
    fixme(guyhod): should be a generetad function. This function should be generated at cunstruction phase based on list of commands (should pass when __init__ is callled).

    Args:
      data (json): AI answer formatted as Json

    Returns:
      None
    """
    command_name, args = self.parse_command(data)
    command = command_name.upper()

    if command == self.config.COMMAND_END_FLOW:
      self.state = self.config.STATE_CONTINUE

  def append_to_file(self, text: str) -> None:
    file_path = path.join("outputs/", self.config.output_file_name)
    f = open(file_path, "a")
    f.write(text + "\n")
    f.close()