import openai
import os

from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("API_KEY", "")

model_list = openai.Model.list()["data"]
print(f"----- Total {str(len(model_list))} models. list of all models:")
print([item["root"] for item in model_list])

gpt_models = []
for item in model_list:
    if 'gpt' in item["root"].lower():
        gpt_models.append(item["root"])
print("----------------------------------")
print(f"----- Total {len(gpt_models )} GPT  models. list of all GPT models:")
print(gpt_models)
