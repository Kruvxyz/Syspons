from pipeline.flows.abstract.generic_flow import AbstractFlow
from typing import Any, Callable, Dict, List, Optional, Tuple
from pipeline.shared_content import current_chat, history, status


# Flow:
# Simulation -> though --> mind --> continue / execute / move next
#
# Explain
#
# for each agent:
# define: history stack
# inputs: json
# build message (prompt_generator[json->str])
#
# input message
#       "on_hold": {},
#       "next": self.agents["init"],  # Temporary thing
#       "situation": self.observation.get(),
#       "content": content


class Consciousness(AbstractFlow):
  def __init__(self,
               config: "Config",
               agents: Dict[str, "Agent"],
               api: "TBD", # an action API
               observation: "TBD" # an observation API
    ) -> None:
    super().__init__(config)
    self.agents = agents
    self.current_agent = self.agents.get("SIMULATION", None)
    assert type(self.current_agent) != type(None), "Failed to load initial agent"

    self.input = ""
    self.mem = []
    self.state: str = self.config.STATE_NONE
    self.set_agent_dict()
    self.api = api
    self.observation = observation

  def pre_execute_loop(self, content: str) -> None:
    """
    Update self params befor executing loop
    """
    self.input = {
      "on_hold": {},
      "next": self.agents["THINK"], 
      "situation": "", #self.observation.get(),
      "content": content
    }
    self.current_agent = self.agents["SIMULATION"]
    self.state = self.config.STATE_RUN
    status.status = self.config.STATE_RUN

  def clear(self) -> None:
    self.agent_dict["THINK"].reset()
    self.agent_dict["SIMULATION"].rese()
    self.agent_dict["MIND"].reset()
    self.pre_execute_loop()
    self.mem = []
    #fixme(guyhod) - fill function
    #...

  def execute(self, data: Dict[str,Any]) -> None:
    """
    Execute command
    """
    current_agent = self.agent_dict[self.current_agent].upper()
    status.agent = current_agent
    command_name, args = self.parse_command(data)
    command = command_name.upper()

    if current_agent == "THINK":
      # agent will make a suggestion
      if command == "ASK" or command == "SUGGEST":
        self.input["on_hold"] = data
        self.current_agent = self.agents["MIND"]
        self.input["next"] = self.agents["SIMULATION"]
        self.mem.append({"THINK": data})
        if command == "ASK":
          self.input["content"] = f"You should simulate a response for: {args['question']}"
        elif command == "SUGGEST":
          self.input["content"] = f"YOu should simulate a response for this action: {args['suggestion']}"

      elif command == self.config.COMMAND_FLAG:
        pass

      else:
        pass

    elif current_agent == "SIMULATION":
      # agent will simulate outcame based on thinking and current state
      self.mem.append({"SIMULATION": data})
      self.current_agent = self.agents["THINK"]
      #fixme(guyhod) - keep going here...

    elif current_agent == "MIND":
      # Update shared content
      if command != "CONTINUE":
        history.append(current_chat)
        current_chat = []

      if command == "CONTINUE":
        # self.current_agent = self.input["next"]
        self.current_agent = self.agent_dict["SIMULATION"]
        #fixme(guyhod) - should parse this based on next agent
        self.pre_execute_loop()
        self.input["content"] = self.input["on_hold"]

      elif command == "SELECT":
        # self.api.execute(self.input["on_hold"], self.mem)
        self.agent_dict["THINK"].trian()
        self.pre_execute_loop()

      elif command == "NEXT":
        self.clear()

      else:
        pass

    else:
      print("rerun...")


    # ### EXAMPLE
    #
    # command_name, args = self.parse_command(data)
    # command = command_name.upper()
    #
    # if command == self.config.COMMAND_END_FLOW:
    #   self.state = self.config.STATE_CONTINUE
    #
    # elif command == self.config.COMMAND_FLAG:
    #   print(f"""Flag content {args}""")
    #   self.state = self.config.STATE_CONTINUE
    #
    # elif command == self.config.COMMAND_STORE_AND_END_FLOW:
    #   self.append_to_file(args.get("summary", ""))
    #   self.state = self.config.STATE_CONTINUE
    #
    # elif command == self.config.COMMAND_SUMMARY:
    #   self.current_agent = self.agents["questions"]
    #
    # elif command == self.config.COMMAND_ANSWER:
    #   self.append_to_file(str(args))
    #   self.state = self.config.STATE_CONTINUE
    #
    # else:
    #   print(f"undefined command {command} with content {args}")
    #   print("rerun...")