import time
import requests

from typing import Dict


class LlamaAsyncInterface:
    def __init__(self, ai_server: str) -> None:
        self.ai_server = f"http://{ai_server}"

    def query(self, system_prompt: str, agent_prompt: str) -> Dict[str, str]:
        resp = requests.post(
            f"{self.ai_server}/query", json={"system": system_prompt, "prompt": agent_prompt})
        resp_json = resp.json()

        if resp_json["status"] != "ok":
            raise Exception(f"server {self.ai_server} communication failed")

        id = resp_json["id"]
        while True:
            resp = requests.post(
                f"{self.ai_server}/read", json={"id": str(id)})
            resp_json = resp.json()
            if resp_json["status"] == "ok":
                return resp_json
            elif resp_json["status"] == "wait":
                pass
            else:
                raise Exception(f"server {self.ai_server} query failed")
            time.sleep(20)
