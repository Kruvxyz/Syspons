"""Syspons FSM : a system to summary and answear documents"""
from fsm.config.config import config
from fsm.flow.main_flow import Flow1Domain
from fsm.agent.agent import Agent
from fsm.agent.resources import gen_system_message
import click
import openai


@click.command()
@click.option(
    "--file",
    type=str,
    help="path to file",
)
def main(file):
    openai.api_key = config.open_ai_key
    # agent_domain_question = Agent(ai=openai, system_prompt=gen_system_message(""), commands=[])
    # def gen_talk(agent):
    #     def talk(content):
    #         self=agent
    #         return """
    #             {
    #             "command": {
    #                 "name": "STORE_AND_END_FLOW",
    #                 "args": {
    #                 "summary": "{""" + content + """}"
    #                 }
    #             }
    #         }
    #         """
    #     return talk
    # agent_domain_summary = Agent(ai=openai, system_prompt="", commands=[])
    # agent_domain_summary.talk = gen_talk(agent_domain_summary)


    raw_document = None #fixme: consume document

    agent_domain_exists = gen_agent_domain_exists(openai)
    agent_domain_question = gen_agent_question(openai)
    flow1_domain_name = Flow1Domain(config, agents = {"init": agent_domain_exists, "questions": agent_domain_question}, file_name=file)

    # Make experiments on tested domain
    chunk_of_text = """
    A private survey of business activity in China’s services sector fell to its lowest level in eight months in August, as a flurry of economic stimulus measures seemed unable to reignite consumption demand.
    The Caixin China general services purchasing managers index (PMI) slipped to 51.8 last month from 54.1 in July, according to data released Tuesday by Caixin Media and S&P Global. A reading above 50 indicates expansion, while anything below that level shows contraction.
    “The slowdown in business activity coincided with a weaker increase in overall new business. New orders increased modestly, and at a pace that was below the average seen for 2023 to date,” Caixin and S&P said in a statement.
    This was partly due to weaker foreign demand for Chinese services, they added, citing evidence of sluggish overseas orders.
    The result was largely in line with the official August PMI data released last week by the National Bureau of Statistics (NBS), which showed slowing demand for services. The sub-index for the services industry, the biggest source of employment for younger people, fell to the lowest level last month since January, according to the NBS, and was far below pre-pandemic levels.
    Compared to the official survey, the Caixin/S&P gauge focuses on smaller businesses and private companies.
    """

    flow1_domain_name.run(chunk_of_text)


def gen_agent_domain_exists(ai):
    agent_domain_exists_system_message = """
    You are an expert in the domain of programing. You will receive partial text and you should decide if text contain information about the object oriented programing or not.

    GOALS:
    Read text carfully.
    Decide if text contain information about Object Oriented Programing (OOP).
    Choose the command best answers if domain information exists in text.

    Constraints:
    No user assistance
    Exclusively use the commands listed in double quotes e.g. "command name"

    Commands:
    end_of_flow: "Text doesn't contain any domain information", args:
    summary: "Text contains domain information", args:
    flag: "Can't decide if text contains domain information", args: "reasoning": "<why you can not make a decision>"


    Performance Evaluation:
    You are to make sure commands use informative argument and not generic naming or uses brakets to indicate generic arguments.

    You should only respond in JSON format as described below Response Format: { "thoughts": { "text": "thought", "reasoning": "reasoning", "plan": "- short bulleted\n- list that conveys\n- long-term plan", "criticism": "constructive self-criticism", "speak": "thoughts summary to say to user" }, "command": { "name": "command name", "args": { "arg name": "value" } } }
    example when text contains information:
    {
        "command": {
            "name": "summary",
            "args": {}
        }
    }

    example when text doesn't contain information:
    {
        "command": {
            "name": "end_of_flow",
            "args": {}
        }
    }

    example if cannot evaluate text:
    {
        "command": {
            "name": "flag",
            "args": {
                "reasoning": "Text is too short and out of context therefore as an expert in the domain I can not guarantee that text contain information about domain"
            }
        }
    }
    Ensure the response can be parsed by Python json.loads
    """
    return Agent(ai=ai, system_prompt=agent_domain_exists_system_message, commands=[])


def gen_agent_question(ai):
    agent_domain_question_system_message = """
    You are an historian with an experty at international relationship (specializes in the Soviet Union).
    You will receive partial text and you should decide if text contain information about the ongoing war in Ukraine.
    Uupdate list of revenlt players in the conflict (not exclusive):
    Vladimir Putin - President of Russia
    Volodymyr Zelenskyy - President of Ukraine


    GOALS:
    Read text carfully.
    Decide if text contain information about Ukraine war.
    Choose the command best answers if domain information exists in text.

    Constraints:
    No user assistance
    Exclusively use the commands listed in double quotes e.g. "command name"

    Commands:
    end_of_flow: "Text doesn't contain any domain information", args:
    summary: "Text contains domain information", args:
    flag: "Can't decide if text contains domain information", args: "reasoning": "<why you can not make a decision>"


    Performance Evaluation:
    You are to make sure commands use informative argument and not generic naming or uses brakets to indicate generic arguments.

    You should only respond in JSON format as described below Response Format: { "thoughts": { "text": "thought", "reasoning": "reasoning", "plan": "- short bulleted\n- list that conveys\n- long-term plan", "criticism": "constructive self-criticism", "speak": "thoughts summary to say to user" }, "command": { "name": "command name", "args": { "arg name": "value" } } }
    example when text contains information:
    {
        "command": {
            "name": "summary",
            "args": {
                "reasoning": "Text articulates the subject of Crimean Peninsula which is part of the Russian-Ukraine conflict."
            }
        }
    }

    example when text doesn't contain information:
    {
        "command": {
            "name": "end_of_flow",
            "args": {
                "reasoning": "Text is focus on tech company and doesn't mention any subject relate to the ongoing war, Russia or Ukriane"
            }
        }
    }

    example if cannot evaluate text:
    {
        "command": {
            "name": "flag",
            "args": {
                "reasoning": "Text is too short and out of context therefore as an expert in the domain I can not guarantee that text contain information about domain"
            }
        }
    }
    Ensure the response can be parsed by Python json.loads

    """
    return Agent(ai=ai, system_prompt=agent_domain_question_system_message, commands=[])
     