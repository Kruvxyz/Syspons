from pipeline.flows.abstract.generic_flow import AbstractFlow
from pipeline.commads import scrape_text_with_selenium
from typing import Any, Callable, Dict, List, Optional, Tuple
from pipeline.agent.agent import Agent


class FlowStocks(AbstractFlow):
  def __init__(self,
               config: "Config",
               agents: Dict[str, "Agent"]
    ) -> None:
    super().__init__(config)
    self.agents = agents
    self.current_agent = self.agents.get("init", None)
    assert type(self.current_agent) != type(None), "Failed to load initial agent"

    self.input = ""
    self.mem = ""
    self.state: str = self.config.STATE_NONE
    self.set_agent_dict()


  def pre_execute_loop(self, content: str) -> None:
    """
    Update self params befor executing loop
    """
    self.stocks_list = ["AAPL", "GOOGL", "META", "NVDA"]
    self.index = 0
    url = f"https://money.cnn.com/quote/forecast/forecast.html?symb={self.stocks_list[self.index]}"
    self.input = scrape_text_with_selenium(url)
    self.current_agent = self.agents["init"]
    self.state = self.config.STATE_RUN

  def execute(self, data: Dict[str,Any]) -> None:
    """
    Execute command
    """
    command_name, args = self.parse_command(data)
    command = command_name.upper()

    current_symbol = self.stocks_list[self.index]
    if self.agent_dict[self.current_agent] == "init":

        if command == self.config.COMMAND_STORE:
           print(f"{current_symbol} -  {str(args)}")
           self.append_to_file(f"{current_symbol} -  {str(args)}")

        else:
           print(f"{current_symbol} - FLAG - {str(args)}")
           self.append_to_file(f"{current_symbol} - FLAG - {str(args)}")

        # progress the program
        if self.index < len(self.stocks_list) - 1:
            self.index += 1
            url = f"https://money.cnn.com/quote/forecast/forecast.html?symb={self.stocks_list[self.index]}"
            self.input = scrape_text_with_selenium(url)

        else:
            # TEMPORARY
            self.state = self.config.STATE_CONTINUE 
            # self.current_agent = self.agents["evaluate"]
    
    elif self.agent_dict[self.current_agent] == "event_collection":
       self.state = self.config.STATE_CONTINUE

    elif self.agent_dict[self.current_agent] == "evaluate":
       self.state = self.config.STATE_CONTINUE
       

    # if command == self.config.COMMAND_END_FLOW:
    #   self.state = self.config.STATE_CONTINUE

    # elif command == self.config.COMMAND_FLAG:
    #   print(f"""Flag content {args}""")
    #   self.state = self.config.STATE_CONTINUE

    # elif command == self.config.COMMAND_STORE_AND_END_FLOW:
    #   self.append_to_file(args.get("summary", ""))
    #   self.state = self.config.STATE_CONTINUE

    # elif command == self.config.COMMAND_SUMMARY:
    #   self.current_agent = self.agents["questions"]

    # elif command == self.config.COMMAND_ANSWER:
    #   url = args.get["symbol"]
    #   scrape_text_with_selenium()
    # #   self.append_to_file(str(args))
    # #   self.state = self.config.STATE_CONTINUE

    else:
      print(f"undefined agent with command {command} and content {args}")
      print("rerun...")

def gen_agent_parse_stocks(ai):
    system_message = """
You are an analyist, expert in stock market. You will receive a text describe a stock shouold parse the following information from text: stock symbol, current value, Stock Price Forecast high median and low, Analyst Recommendations to outperform, buy, hold, sell and underperform.

GOALS:
Read text carfully.
Parse the information currectly as passible, if not passible mark FLAG.
Exclusively use the commands listed in double quotes e.g. "command name"

Commands:
store: "parse succefully", args: "symbol": "<SYMBOL>", "current_value": "<value>", "prediction": { "high": "<high price prediction>", "median": "<median price prediction>", "low": "<low price prediction>" }, "recommendations": { "number_of_analyists": "<number of analyists to recommend>", "recommendation": "<analyists recommendation>"}
flag: "Can't answer", args: "reasoning": "<why you can not make a decision>"

Constraints:
No user assistance
Exclusively use the json format to listed the information in double quotes e.g. "stock symbol"

Performance Evaluation:
You are to make sure json is informative and accurate as possible, it is better to mark FLAG then incorrect information.

You should only respond in JSON format as described below Response Format: { "command": { "name": "command name", "args": { "arg name": "value" } } }

example when text contains information:
{
    "command": {
        "name": "store",
        "args": {
            "symbol": "AAPL",
            "current_value": "100",
            "prediction": {
                "high": "140",
                "median": "120",
                "low": "90"
            }
            "recommendations": {
                "number_of_analyists": 40,
                "recommendation": "buy"
            } 
    }
}

example when text information is not clear:
{
    "command": {
        "name": "flag",
        "args": {
            "reasoning": "Text context is unclear"
        }
    }
}

Ensure the response can be parsed by Python json.loads
    """
    return Agent(ai=ai, system_prompt=system_message, commands=[])

# agent = gen_agent_parse_stocks(openai)
# flow = FlowStocks(config, agents={"init": agent})
# flow.run("")
