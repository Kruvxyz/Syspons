import unittest
from pipeline.functions.ParseToJson import loadString


class TestParseToJson(unittest.TestCase):
    def simple_dict_paring(self):
        count_apples = 3
        count_organes = 5
        text = f'{"apple": {count_apples}, "cars": {count_organes}}'
        format = {"apples": "num of apples default 0",
                  "cars": "num of cars default 0"}
        parsed = loadString(text, format, attemps=1)
        self.assertEqual(int(parsed["apples"]), count_apples)
        self.assertEqual(int(parsed["oranges"]), count_organes)

    def test_parsing_fruits(self):
        count_apples = 3
        count_organes = 5
        text = f"apples: {count_apples}.\n oranges: {count_organes}."
        format = {
            "fruits": {
                "apples": "num of apples  default 0",
                "oranges": "num of oranges default 0",
                "bannas": "num of bannaes default 0"},
            "cars": {
                "lamburgini": "num of lamburinis default 0",
                "toyotas": "number of toyotas default 0"
            }
        }

        parsed = loadString(text, format)
        self.assertEqual(int(parsed["fruits"]["apples"]), count_apples)
        self.assertEqual(int(parsed["fruits"]["oranges"]), count_organes)

    def parse_text(self):
        name = "John Smith"
        city = "Tel Aviv"
        text = f"my name is {name}, I live in {city}"
        format = {
            "name": "your name default None",
            "city": "city you live in default None",
            "Phone number": "your phone number default None"
        }

        parsed = loadString(text, format)
        self.assertEqual(parsed["name"], name)
        self.assertEqual(parsed["city"], city)
