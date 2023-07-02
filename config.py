import os
from dotenv import load_dotenv

load_dotenv()

PAS_BASE = os.getenv('pas_base')
SECRET_KEY = os.getenv('secret_key')
