from api import EthereumAPI
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    load_dotenv()  # load .env file
    endpoint_url = os.getenv("ENDPOINT_URL")

    # create an instance of EthereumAPI
    ethereum_api = EthereumAPI(endpoint_url)

    # define ethereum block range
    start_block = 18908800
    end_block = 18909050




