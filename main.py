from api import EthereumAPI
from constants import endpoint_url

if __name__ == "__main__":

    # create an instance of EthereumAPI
    ethereum_api = EthereumAPI(endpoint_url)

    # define ethereum block range
    start_block = 18908800
    end_block = 18909050
