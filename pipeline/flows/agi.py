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
import time

class Consciousness(AbstractFlow):
  def __init__(self,
               config: "Config",
               agents: Dict[str, "Agent"],
               api: "TBD", # an action API
               observation: "TBD" # an observation API
    ) -> None:
    super().__init__(config)
    self.agents = agents
    self.current_agent = self.agents.get("DM", None)
    assert type(self.current_agent) != type(None), "Failed to load initial agent"

    self.input = ""
    self.mem = []
    self.state: str = self.config.STATE_NONE
    self.set_agent_dict()
    self.api = api
    self.observation = observation

  def pre_execute_loop(self, content: str = "") -> None:
    """
    Update self params befor executing loop
    """
    self.input = {
      "first_run": True,
      "on_hold": {},
      "text": "",
      "next": self.agents["THOUGHT_FACTORY"], 
      "situation": "", #self.observation.get(),
      "content": content,
      "prediction" : ""
    }
    self.current_agent = self.agents["DM"]
    self.state = self.config.STATE_RUN
    status.status = self.config.STATE_RUN

  def clear(self) -> None:
    self.agent_dict["THOUGHT_FACTORY"].reset()
    self.agent_dict["SIMULATION"].reset()
    self.agent_dict["GATE_KEEPER"].reset()
    self.agent_dict["DM"].reset()
    self.pre_execute_loop()
    self.mem = []
    #fixme(guyhod) - fill function
    #... --> is there something else i need to do here?
    # consider closing this

  def execute(self, data: Dict[str,Any]) -> None:
    """
    Execute command
    """
    current_agent = self.agent_dict[self.current_agent].upper()
    status.agent = current_agent
    # time.sleep(60) # save guard from OPENAI token limitation

    if current_agent == "THOUGHT_FACTORY":
      reasoning = data.get("reasoning", "")
      prediction = data.get("prediction", "")
      action = data["action"]

      content = f"""
action: 
{action}

reasoning: 
{reasoning}
"""
      self.input["content"] = content

      print(action)
      self.current_agent = self.agents["SIMULATION"]


    elif current_agent == "SIMULATION":
      prediction = data["prediction"]
      # self.mem.append({"SIMULATION": data})

      self.input["prediction"] = prediction

      print(prediction)
      self.current_agent = self.agents["GATE_KEEPER"]

    elif current_agent == "GATE_KEEPER":
      command_name, args = self.parse_command(data)
      command = command_name.upper()
      question = data.get("question", "")

      if command == "REFLECT":
        # history.append(current_chat)
        # current_chat = []
        content = self.input["content"]
        self.input["text"] = f"""
based on your:
{content}


Try to convince me by answering this question:
{question}
        """

        self.current_agent = self.agents["THOUGHT_FACTORY"]


      if command == "EXECUTE":
        # self.current_agent = self.input["next"]
        #fixme(guyhod) - should parse this based on next agent
        # self.pre_execute_loop()
        # self.input["content"] = self.input["on_hold"]

        # nothing to do
        self.input["text"] = ""
        self.current_agent = self.agents["DM"]


      elif command == "AVOID":
        # self.api.execute(self.input["on_hold"], self.mem)
        # self.agent_dict["THINK"].trian()
        # self.pre_execute_loop()

        self.input["text"] = ""          
        self.input["content"] = "Player did nothing"
        self.current_agent = self.agents["DM"]



      else:
        # punish
        self.input["text"] = ""          
        self.input["content"] = "Player did nothing"
        self.current_agent = self.agents["DM"]

        print("fail to call command, rerun")
        #fixme: should add a critic here

    elif current_agent == "DM":
      Previously = data.get("Previously", "")
      now = data.get("now", "")
      options = data.get("options", "")

      self.input["first_run"] = False
      self.input["situation"] = f""" 
Previously:
{Previously}

The situation is:
{now}

Your options are:
{options}
"""
      self.input["text"] = ""
      print(now)
      self.current_agent = self.agents["THOUGHT_FACTORY"]

    else:
      print("rerun...")
