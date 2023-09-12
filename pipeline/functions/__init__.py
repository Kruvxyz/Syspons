import json
import tiktoken
from typing import Any, Callable, Dict, List, Optional, Tuple


def ParseResponse(response: str) -> Dict[str, str]:
  """
  This function parse the LLM response and return a JSON.
  Exapmles: https://github.com/Kruvxyz/Auto-GPT/blob/stable/autogpt/json_utils/json_fix_llm.py (fix_json_using_multiple_techniques)
  """
  return json.loads(response)


encoding = tiktoken.encoding_for_model("gpt-4")

def count_tokens(text: str) -> int:
  """Count number of tokens in text.

  Args:
      text (str): Text to count

  Returns:
      int: number of tokens in text
  """
  return len(encoding.encode(text))