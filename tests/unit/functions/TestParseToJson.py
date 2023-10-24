import unittest
from pipeline.functions.ParseToJson import loadString


class TestParseToJson(unittest.TestCase):
    """
    Testing by verify no error is raised
    """
    def simple_dict_paring(self):
        text = '{"apple": 4, "cars": 1}'
        format = {"apples": "num of apples default 0", "cars": "num of cars default 0"}
        loadString(text, format, attemps=1)

    def test_parsing_fruits(self):
        text = "apples: 3, oranges: 5"
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

        loadString(text, format)


    def parse_text(self):
        text = "my name is John Smith, I live in Tel Aviv"
        format = {
            "name": "your name default None",
            "city": "city you live in default None",
            "Phone number": "your phone number default None"
        }

        loadString(text, format)
