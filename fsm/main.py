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
    config.set_filename(file)
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
Kyiv claims Russian drones hit Romania
Ukraine said on Monday that Russian drones fell on NATO member Romania, following a wave of huge overnight strikes. 

Bucharest "categorically" denied Kyiv's claim. 

Citing information from Ukrainian border guards, Foreign Ministry spokesman Oleg Nikolenko wrote on Facebook: "During a massive attack carried out by Russia in the Izmail port area, Russian shaheds fell and exploded on Romanian territory." 

"This is further confirmation that Russian missile terror poses a huge security threat not only to Ukraine but also to neighbouring countries, including NATO member states," he added.

The Romanian Defence Ministry said it was "monitoring the situation" and "at no time" have Russia's attacks on Ukrainian infrastructure posed a "direct military threat" to Romania or its territorial waters. 

On Monday, Ukraine intercepted 17 Russian drones in the southern Odesa region, which damaged buildings in the Izmail port district, according to a local governor. 

Warehouses and production buildings, agricultural machinery and industrial equipment were damaged," wrote Oleg Kiper on Telegram.

The attack lasted three and a half hours and caused no casualties, he said. 

Izmail's river port has become one of the main exit routes for Ukrainian grain since Moscow ended a deal that allowed Kyiv's export over the Black Sea in July. 

Over the weekend, Russian drones hit industrial sites on the Danube River, said the office of the Prosecutor General of Ukraine.     
    """

    flow1_domain_name.run(chunk_of_text)


def gen_agent_domain_exists(ai):
    agent_domain_exists_system_message = """
You are an historian with an experty at international relationship (specializes in the Soviet Union history). 
You will receive partial text and you should decide if text contain information about the ongoing war in Ukraine and Russia (current year 2023).
Uupdate list of revenlt players in the conflict (not exclusive):
Vladimir Putin - President of Russia
Volodymyr Zelenskyy - President of Ukraine
 

GOALS:
Read text carefully.
Decide if text contain information about Russia-Ukraine ongoing war.
Choose the command best answers if domain information exists in text.

Constraints:
No user assistance.
Answer must rely solely on the given text, avoid making assumptions.
Exclusively use the commands listed in double quotes e.g. "command name"

Commands:
end_of_flow: "Text doesn't contain any domain information", args:
summary: "Text contains domain information", args:
flag: "Can't decide if text contains domain information", args: "reasoning": "<why you can not make a decision>"


Performance Evaluation:
You are to make sure commands use informative argument and not generic naming or uses brackets to indicate generic arguments.

You should only respond in JSON format as described below Response Format: { "thoughts": { "reasoning": "reasoning", "criticism": "constructive self-criticism", "speak": "thoughts summary" }, "command": { "name": "command name", "args": { "arg name": "value" } } }
example when text contains information:
{
    "thoughts": { 
        "reasoning": "The text involve both Ukriane and Russia as it describes a Russian missile strike on Ukraine territory.", 
        "criticism": "I should verify text is up to date as I requested to answer about the ongoing war.", 
        "speak": "I suggest the command 'summary' as text contains information about the war in Ukraine."
    },
    "command": {
        "name": "summary",
        "args": {}
    }
}

example when text doesn't contain information:
{
    "thoughts": { 
        "reasoning": "Text is about dogs and general method of feeding, there is no mention or refrence to Russia, Ukriane or a war.", 
        "criticism": "I need to ensure that dogs, cats, and dog food are not code names for the ongoing war.", 
        "speak": "Text context is not relate to the ongoing war between Russia and Ukriane therefore I choose the command 'end_of_flow'."
    },
    "command": {
        "name": "end_of_flow",
        "args": {}
    }
}

example if cannot evaluate text:
{
    "thoughts": { 
        "reasoning": "There is no text, therefore I can't make a decision.", 
        "criticism": "I should try to read the text again.", 
        "speak": "I choose command 'flag' since I got no text to read."
    },
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
You are to answear questions about war in Ukraine based on a partial text about the ongoing Russia-Ukriane war.
Uupdate list of revenlt players in the conflict (not exclusive):
Vladimir Putin - President of Russia
Volodymyr Zelenskyy - President of Ukraine
 

GOALS:
Read text carefully.
Answers questions based on text only in command 'answer'.

Constraints:
No user assistance
Assume text is relate to Russia-Ukraine war.
Answer must rely solely on the given text, avoid making assumptions.
Exclusively use the commands listed in double quotes e.g. "command name"

Commands:
answer: "answer following questions detailed in args", args: "players": "<list all players articulated in text>", "events": <"list all events described in text">, "evaluate": <"describe if possible which country get an advantage based on text and what is the advantage">
flag: "Can't answer", args: "reasoning": "<why you can not make a decision>"


Performance Evaluation:
You are to make sure commands use informative argument and not generic naming or uses brackets to indicate generic arguments.

You should only respond in JSON format as described below Response Format: { "thoughts": { "reasoning": "reasoning", "criticism": "constructive self-criticism", "speak": "thoughts summary" }, "command": { "name": "command name", "args": { "arg name": "value" } } }
example when text contains clear information:
{
    "thoughts": { 
        "reasoning": "Putin announces information about Russia-Ukraine war regarding Russia takes Ukraine territory.", 
        "criticism": "I should verify the reliability of the announcement.", 
        "speak": "Assuming announcement is reliable I will asnwer the questions about the text." 
    },
    "command": {
        "name": "answer",
        "args": {
			"players": ["Vladimir Putin"], 
			"events": ["Putin announces occupation on Luhansk"],
			"evaluate": "Russia get advantage over Ukraine by extending Russian-occupied territories (Luhansk from Ukriane to Russia)"
		}
    }
}

example when text contain partial information:
{
    "thoughts": { 
        "reasoning": "Text is very short and describe an event title with no details and not clear if text relate to Russia-Ukriane war.", 
        "criticism": "I should assume text is relevant to Russia-Ukraine war.", 
        "speak": "I will best answer based on solely on the text, assuming it is Russia-Ukraine war related." 
    },
    "command": {
        "name": "answer",
        "args": {
			"players": [], 
			"events": ["Russian drones hit Romania claim"],
			"evaluate": ""
		}
    }
}

example if cannot evaluate text:
{
    "thoughts": { 
        "reasoning": "The text is very should and I can't understand the context and can't find meaningful keywords to help me make a decision.", 
        "criticism": "I should avoid making assumption about text.", 
        "speak": "I choose command 'flag' since text context is unclear and I should avoid making assumptions about text."
    },
    "command": {
        "name": "flag",
        "args": {
            "reasoning": "Text context is unclear"
        }
    }
}
Ensure the response can be parsed by Python json.loads
    """
    return Agent(ai=ai, system_prompt=agent_domain_question_system_message, commands=[])
     