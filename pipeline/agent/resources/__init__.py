import json
from typing import Any, Callable, Dict, List, Optional, Tuple

elements = {
    "GOALS": [
        "Read text carfully.",
        "Decide if text contain information about Object Oriented Programing (OOP).",
        "Choose the command best answers if domain information exists in text."
    ],
    "Constraints": [
        "No user assistance",
        'Exclusively use the commands listed in double quotes e.g. "command name"'
    ],
    "Commands": [
        """end_of_flow: "Text doesn't contain any domain information", args:""",
        """summary: "Text contains domain information", args:""",
        """flag: "Can't decide if text contains domain information", args: "reasoning": "<why you can not make a decision>"""
    ],
    "Performance Evaluation":[
        """You are to make sure commands use informative argument and not generic naming or uses brakets to indicate generic arguments."""
    ]

}


def get_definition() -> str:
  return """You are an expert in the domain of programing. You will receive partial text and you should decide if text contain information about the object oriented programing or not.\n"""

def get_requirements(elements: Dict[str, List[str]]) -> str:
  requirements = ""
  for element in elements:
    requirements += element + ":\n"
    for item in elements[element]:
      requirements += item + "\n"
    requirements += "\n"
  return requirements

def get_format(elements: Dict[str, List[str]]):
  format = {
       "thoughts": {
            "text": "thought",
            "reasoning": "reasoning",
            "plan": "- short bulleted\n- list that conveys\n- long-term plan",
            "criticism": "constructive self-criticism",
            "speak": "thoughts summary to rationalize command"
        },
       "command": {
          "name": "command name",
          "args": { "arg name": "value" }
        }
  }
  listed_elements = []
  for key, value in elements.items():
    listed_elements += value
  # listed_elements = [(item for item in elements[element]) for element in elements]
  format["evaluate"] = {element: f"grade element {element}'s significance from 0 to 100" for element in listed_elements}
  # format["evaluate"] = {element: f"grade element {element}'s significance from 0 to 100" for element in elements}
  # format["evaluate"] = {element: f"grade element {element}'s significance from 0 to 100" for item in element
  #                       for element in elements}

  return f"""
You should only respond in JSON format as described below Response Format:
{str(json.dumps(format))}
Ensure the response can be parsed by Python json.loads
  """

def gen_system_message(text):
  generic_text = f"""
{get_definition()}
{get_requirements(elements)}
{get_format(elements)}
  """
  # format = get_format()
  return generic_text