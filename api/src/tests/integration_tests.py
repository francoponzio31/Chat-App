import unittest
import requests
from dotenv import load_dotenv
from ..utilities.utils import get_env_value



class TestChatAPI(unittest.TestCase):

    load_dotenv()
    BASE_URL = get_env_value("BASE_URL")