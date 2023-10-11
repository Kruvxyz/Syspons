from singleton_decorator import singleton
from dotenv import load_dotenv
import logging
import os

load_dotenv()

logging_file = os.getenv("LOGGING_FILE", "logs.log")
logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s',
                    filename=f"logs/{logging_file}", level=logging.DEBUG)
logger = logging.getLogger(__name__)


@singleton
class Status:
    def __init__(self):
        self.agent = ""
        self.status = ""


status = Status()
agents = {}
