from dotenv import load_dotenv
import os

load_dotenv()  # load .env file
endpoint_url = os.getenv("ENDPOINT_URL")
