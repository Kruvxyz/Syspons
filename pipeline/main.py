"""Syspons FSM : a system to summary and answear documents"""
from pipeline.config.config import config
# from pipeline.flows.main_flow import Flow1Domain
from pipeline.flows.simple_flow_2 import OneStepFlow
from pipeline.functions import count_tokens
from pipeline.agent.agent import Agent
from pipeline.agent.resources import gen_system_message
from pipeline.functions.ParseWord import headers, parse_docx, chunk_dict, chunk_dict_with_headers
from pipeline.functions.FilesInFolder import get_files
from pipeline.functions.LlamaAsyncInterface import LlamaAsyncInterface
import click
import os
import os.path as path
import openai
import zipfile
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from PyPDF2 import PdfReader 

from pipeline.shared_content import status


load_dotenv()
config.ai["provider"] = os.getenv("LLM_PROVIDER")
config.open_ai_key = os.getenv("API_KEY", "")
config.model = os.getenv("OPENAI_MODEL", "gpt-4")
config.ai["model"] = config.model


@click.command()
@click.option(
    "--file",
    type=str,
    default="",
    help="path to file",
)
@click.option(
    "--folder",
    type=str,
    default="",
    help="path to files' folder",
)
@click.option(
    "--file_type",
    type=str,
    default="txt",
    help="type of file parsing",
)
@click.option(
    "--output",
    type=str,
    default="output.txt",
    help="name of output file",
)
def main(file: str, folder: str, output: str, file_type: str) -> None:
    status.status="run"
    if len(file)==0:
        files = get_files(folder, filter=file_type)
        config.set_filenames(files)
    else:
        doc_path = path.join("documents/", file)
        config.set_filenames([doc_path])
    config.set_output_filename(output)

    if config.ai["provider"] == 'openai':
        openai.api_key = config.open_ai_key
        config.ai["ai"] = openai
    elif config.ai["provider"] == 'llama2':
        ai_server = os.getenv("LLAMA_ADDRESS")
        config.ai["ai"] = LlamaAsyncInterface(ai_server=ai_server)
    
    from pipeline.agent.instantiations.agent_syspons_1 import syspons_agent_1

    BUFFER = 0
    
    for doc_path in config.file_names:
    # fixme(guyhod): should be done based on tokens
        if file_type == 'txt':
            doc = open(doc_path, "r")
            raw_document = doc.read()
            chunk_size = 10000
            chunks = [{"header": "None", "data": raw_document[i:i+chunk_size]}
                for i in range(0, len(raw_document), chunk_size)]
            
        elif file_type == 'word':
            json_doc = parse_docx(doc_path)
            # chunks = chunk_dict(json_doc)
            chunks = chunk_dict_with_headers(json_doc)

        elif file_type == 'pdf':
            reader = PdfReader(doc_path) 
            pages_docuemnt = [page.extract_text() for page in reader.pages]
            raw_document = ' '.join(pages_docuemnt)
            chunk_size = 10000
            chunks = [{"header": "None", "data": raw_document[i:i+chunk_size]}
                for i in range(0, len(raw_document), chunk_size)]            

        # agent_domain_exists = gen_agent_domain_exists(openai)
        # agent_domain_question = gen_agent_question(openai)


        # flow1_domain_name = Flow1Domain(config, agents = {"init": agent_ukraine_war_in_text, "questions": agent_ukraine_war_questions})
        one_step_flow = OneStepFlow(config, agents={"init": syspons_agent_1})
        # flow1_domain_name = Flow1Domain(config, agents={"init": agent_ukraine_war})



        for index, chunk in enumerate(chunks):
            print(index)
            header = str(chunk["header"])
            data = chunk["data"]
            print(f""" 
    agent max tokens: {syspons_agent_1.get_expected_converation_tokens()}
    docuemnt tokens: {count_tokens(data)}
    buffer: {BUFFER}
    LLM max tokens: {config.max_tokens}
            """)
            print(data)
            if syspons_agent_1.get_expected_converation_tokens() + count_tokens(data) < config.max_tokens + BUFFER:
                one_step_flow.data["filename"] = doc_path
                one_step_flow.data["headers"] = header
                one_step_flow.run(data)

            else:
                print(f"failed for chunk {str(index)} with header {str(header)}")


#     print(f"""
# agent max tokens: {max(agent_ukraine_war_in_text.get_expected_converation_tokens(), agent_ukraine_war_questions.get_expected_converation_tokens())}
# docuemnt tokens: {count_tokens(raw_document)}
# buffer: {BUFFER}
# LLM max tokens: {config.max_tokens}
#     """)
#     if max(agent_ukraine_war_in_text.get_expected_converation_tokens(), agent_ukraine_war_questions.get_expected_converation_tokens()) + count_tokens(raw_document) < config.max_tokens + BUFFER:
#         flow1_domain_name.run(raw_document)


# def gen_agent_domain_exists(ai):
#     agent_domain_exists_system_message = """
# You are an historian with an experty at international relationship (specializes in the Soviet Union history).
# You will receive partial text and you should decide if text contain information about the ongoing war in Ukraine and Russia (current year 2023).
# Update list of revenlt players in the conflict (not exclusive):
# Vladimir Putin - President of Russia
# Volodymyr Zelenskyy - President of Ukraine

# GOALS:
# Read text carefully.
# Decide if text contain information about Russia-Ukraine ongoing war.
# Choose the command best answers if domain information exists in text.

# Constraints:
# No user assistance.
# Answer must rely solely on the given text, avoid making assumptions.
# Exclusively use the commands listed in double quotes e.g. "command name"

# Commands:
# end_of_flow: "Text doesn't contain any domain information", args:
# summary: "Text contains domain information", args:
# flag: "Can't decide if text contains domain information", args: "reasoning": "<why you can not make a decision>"

# Performance Evaluation:
# You are to make sure commands use informative argument and not generic naming or uses brackets to indicate generic arguments.

# You should only respond in JSON format as described below Response Format: { "thoughts": { "reasoning": "reasoning", "criticism": "constructive self-criticism", "speak": "thoughts summary" }, "command": { "name": "command name", "args": { "arg name": "value" } } }
# example when text contains information:
# {
#     "thoughts": {
#         "reasoning": "The text involve both Ukriane and Russia as it describes a Russian missile strike on Ukraine territory.",
#         "criticism": "I should verify text is up to date as I requested to answer about the ongoing war.",
#         "speak": "I suggest the command 'summary' as text contains information about the war in Ukraine."
#     },
#     "command": {
#         "name": "summary",
#         "args": {}
#     }
# }

# example when text doesn't contain information:
# {
#     "thoughts": {
#         "reasoning": "Text is about dogs and general method of feeding, there is no mention or refrence to Russia, Ukriane or a war.",
#         "criticism": "I need to ensure that dogs, cats, and dog food are not code names for the ongoing war.",
#         "speak": "Text context is not relate to the ongoing war between Russia and Ukriane therefore I choose the command 'end_of_flow'."
#     },
#     "command": {
#         "name": "end_of_flow",
#         "args": {}
#     }
# }

# example if cannot evaluate text:
# {
#     "thoughts": {
#         "reasoning": "There is no text, therefore I can't make a decision.",
#         "criticism": "I should try to read the text again.",
#         "speak": "I choose command 'flag' since I got no text to read."
#     },
#     "command": {
#         "name": "flag",
#         "args": {
#             "reasoning": "Text is too short and out of context therefore as an expert in the domain I can not guarantee that text contain information about domain"
#         }
#     }
# }
# Ensure the response can be parsed by Python json.loads
#     """
#     return Agent(ai=ai, system_prompt=agent_domain_exists_system_message, commands=[])


# def gen_agent_question(ai):
#     agent_domain_question_system_message = """
# You are an historian with an experty at international relationship (specializes in the Soviet Union).
# You are to answear questions about war in Ukraine based on a partial text about the ongoing Russia-Ukriane war.
# Update list of revenlt players in the conflict (not exclusive):
# Vladimir Putin - President of Russia
# Volodymyr Zelenskyy - President of Ukraine

# GOALS:
# Read text carefully.
# Answers questions based on text only in command 'answer'.

# Constraints:
# No user assistance
# Assume text is relate to Russia-Ukraine war.
# Answer must rely solely on the given text, avoid making assumptions.
# Exclusively use the commands listed in double quotes e.g. "command name"

# Commands:
# answer: "answer following questions detailed in args", args: "players": "<list all players articulated in text>", "events": <"list all events described in text">, "evaluate": <"describe if possible which country get an advantage based on text and what is the advantage">
# flag: "Can't answer", args: "reasoning": "<why you can not make a decision>"

# Performance Evaluation:
# You are to make sure commands use informative argument and not generic naming or uses brackets to indicate generic arguments.

# You should only respond in JSON format as described below Response Format: { "thoughts": { "reasoning": "reasoning", "criticism": "constructive self-criticism", "speak": "thoughts summary" }, "command": { "name": "command name", "args": { "arg name": "value" } } }
# example when text contains clear information:
# {
#     "thoughts": {
#         "reasoning": "Putin announces information about Russia-Ukraine war regarding Russia takes Ukraine territory.",
#         "criticism": "I should verify the reliability of the announcement.",
#         "speak": "Assuming announcement is reliable I will asnwer the questions about the text."
#     },
#     "command": {
#         "name": "answer",
#         "args": {
# 			"players": ["Vladimir Putin"],
# 			"events": ["Putin announces occupation on Luhansk"],
# 			"evaluate": "Russia get advantage over Ukraine by extending Russian-occupied territories (Luhansk from Ukriane to Russia)"
# 		}
#     }
# }

# example when text contain partial information:
# {
#     "thoughts": {
#         "reasoning": "Text is very short and describe an event title with no details and not clear if text relate to Russia-Ukriane war.",
#         "criticism": "I should assume text is relevant to Russia-Ukraine war.",
#         "speak": "I will best answer based on solely on the text, assuming it is Russia-Ukraine war related."
#     },
#     "command": {
#         "name": "answer",
#         "args": {
# 			"players": [],
# 			"events": ["Russian drones hit Romania claim"],
# 			"evaluate": ""
# 		}
#     }
# }

# example if cannot evaluate text:
# {
#     "thoughts": {
#         "reasoning": "The text is very should and I can't understand the context and can't find meaningful keywords to help me make a decision.",
#         "criticism": "I should avoid making assumption about text.",
#         "speak": "I choose command 'flag' since text context is unclear and I should avoid making assumptions about text."
#     },
#     "command": {
#         "name": "flag",
#         "args": {
#             "reasoning": "Text context is unclear"
#         }
#     }
# }
# Ensure the response can be parsed by Python json.loads
#     """
#     return Agent(ai=ai, system_prompt=agent_domain_question_system_message, commands=[])
