# filepath: 
# ...existing code...
from openai import OpenAI
from dotenv import load_dotenv
import os

class OpenAIClient:
  _instance = None

  def __new__(cls, *args, **kwargs):
    if cls._instance is None:
      cls._instance = super().__new__(cls)
      load_dotenv()  # loads .env if present

      # Read key from environment
      openai_api_key = os.getenv("OPENAI_API_KEY")
      if not openai_api_key:
          raise RuntimeError("OPENAI_API_KEY is not set. Set it (setx or GUI) and restart the app.")

      cls._instance.client = OpenAI(api_key=openai_api_key)
    
    return cls._instance

  def get_client(self):
    return self.client
# ...existing code...