from fsm.flow.abstract.generic_flow import AbstractFlow
from typing import Any, Callable, Dict, List, Optional, Tuple

class Flow1Domain(AbstractFlow):
  def __init__(self,
               config: "Config",
               agents: Dict[str, "Agent"],
               file_name: Optional[str] = None
    ) -> None:
    super().__init__(config)
    self.agents = agents
    self.current_agent = self.agents.get("init", None)
    assert type(self.current_agent) != type(None), "Failed to load initial agent"

    if file_name:
      self.file_name = file_name
    else:
      self.file_name = "output.txt"

    self.input = ""
    self.mem = ""
    self.state: str = self.config.STATE_NONE
    self.set_agent_dict()


  def pre_execute_loop(self, content: str) -> None:
    """
    Update self params befor executing loop
    """
    self.input = content
    self.current_agent = self.agents["init"]
    self.state = self.config.STATE_RUN

  def execute(self, data: Dict[str,Any]) -> None:
    """
    Execute command
    """
    command_name, args = self.parse_command(data)
    command = command_name.upper()

    if command == self.config.COMMAND_END_FLOW:
      self.state = self.config.STATE_CONTINUE

    elif command == self.config.COMMAND_FLAG:
      print(f"""Flag content {args}""")
      self.state = self.config.STATE_CONTINUE

    elif command == self.config.COMMAND_STORE_AND_END_FLOW:
      self.append_to_file(args.get("summary", ""))
      self.state = self.config.STATE_CONTINUE

    elif command == self.config.COMMAND_SUMMARY:
      self.current_agent = self.agents["questions"]

    elif command == self.config.COMMAND_ANSWER:
      self.append_to_file(str(args))
      self.state = self.config.STATE_CONTINUE

    else:
      print(f"undefined command {command} with content {args}")
      print("rerun...")