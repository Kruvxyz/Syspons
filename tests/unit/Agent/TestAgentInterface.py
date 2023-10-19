import unittest
from pipeline.agent.agent import Agent


class ChatCompletion:
    def __init__(self, return_string: str) -> None:
        self.return_string = return_string

    def create(self, *args, **keyargs) -> str:
        response = {
            "choices": [
                {
                    "message": {
                        "content": self.return_string
                    }
                }
            ]
        }
        return response


class AIInterface:
    def __init__(self, return_string):
        self.ChatCompletion = ChatCompletion(return_string)


class TestAgentInterface(unittest.TestCase):
    def test_gen_agent_simple(self):
        return_string = "test string"
        ai_interface = AIInterface(return_string)
        agent = Agent("TEST", ai={"ai": ai_interface, "provider": "openai"}, system_prompt="test", commands=[])
        answer = agent.talk("input")
        self.assertEqual(answer, return_string)

    def test_push_and_reset_agent(self):
        ai_interface = AIInterface("test")
        agent = Agent("TEST", ai={"ai": ai_interface, "provider": "openai"}, system_prompt="test", commands=[])
        agent.push_message({"test":"test"})
        self.assertEqual(agent.history, [{"test":"test"}])
        agent.reset()
        self.assertEqual(agent.history, [])

    def test_prepare_agent_prompt_with_input(self):
        user_input = "test"

        ai_interface = AIInterface("test")
        agent = Agent("TEST", ai={"ai": ai_interface, "provider": "openai"}, system_prompt="test", commands=[])
        prompt = agent.prepare_agent_prompt(user_input)

        self.assertEqual(prompt, user_input)
    
    def test_prepare_agent_prompt_with_data(self):
        user_input = "not this"
        user_data = {"test": "input"}
        expected_prompt = "this!"

        ai_interface = AIInterface("test")
        agent = Agent("TEST", ai={"ai": ai_interface, "provider": "openai"}, system_prompt="test", commands=[], prompt_generator=lambda x: expected_prompt)
        prompt = agent.prepare_agent_prompt(user_input, user_data)
        
        self.assertEqual(prompt, expected_prompt)
    
if __name__ == '__main__':
    unittest.main()
