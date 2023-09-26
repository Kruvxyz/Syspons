import unittest
from pipeline.agent.agent import Agent


class ChatCompletion:
    def __init__(self, return_string: str) -> None:
        self.return_string = return_string

    def create(self, *args, **keyargs) -> str:
        return self.return_string


class AIInterface:
    def __init__(self, return_string):
        self.ChatCompletion = ChatCompletion(return_string)


class TestAgentInterface(unittest.TestCase):
    def test_gen_agent_simple(self):
        return_string = "test string"
        ai_interface = AIInterface(return_string)
        agent = Agent(ai=ai_interface, system_prompt="test")
        answer = agent.talk("input")
        self.assertEqual(answer, return_string)

if __name__ == '__main__':
    unittest.main()