import requests
from pydantic import ValidationError
from api_types import BlockResponse, GetBlockByNumberResponse, Block
import time


class EthereumAPI:
    def __init__(self, endpoint_url):
        self.endpoint_url = endpoint_url

    def send_rpc_request(self, method, params, batch=False):
        """
        sends request to the endpoint. this function has a batch flag that would allow it to send a batch of payloads
        """
        if batch:
            payload = params
        else:
            payload = {"jsonrpc": "2.0", "method": method, "params": params, "id": 1}
        response = requests.post(self.endpoint_url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    def get_block_by_number(self, block_number, include_transactions=True):
        """
        returns info about a single block with the given block number
        """
        method = "eth_getBlockByNumber"
        params = [block_number, include_transactions]
        response = self.send_rpc_request(method, params)
        if response:
            try:
                block_response = GetBlockByNumberResponse(**response)
                return block_response.result
            except ValidationError as e:
                print(f"Error parsing block response: {e}")
                return None

    def get_latest_block_number(self):
        """
        returns the latest block in the blockchain.
        """
        method = "eth_blockNumber"
        params = []
        response = self.send_rpc_request(method, params)
        if response:
            try:
                block_number = BlockResponse(**response)
                return block_number.result
            except ValidationError as e:
                print(f"Error parsing response: {e}")
                return None

    def get_blocks_in_batch(self, from_block, to_block, include_transactions=True):
        """
        calls eth_getBlockByNumber method for blocks in range from_block -> to_block.
        it does include Transaction objects.
        """
        max_requests = 16  # max requests based on 330 credits/sec limit and each method costing 20 credits
        blocks = {}

        # create batches whilst respecting max_requests and then it sends the requests
        for start in range(from_block, to_block + 1, max_requests):
            end = min(start + max_requests, to_block + 1) # calculate end of range
            batches = []
            for block_number in range(start, end): # iterate through current batch and append to current payload
                batches.append(
                    {
                        "jsonrpc": "2.0",
                        "method": "eth_getBlockByNumber",
                        "params": [hex(block_number), include_transactions], # convert block number to hex
                        "id": block_number - from_block, # unique id for each batch
                    }
                )

            response = self.send_rpc_request(
                method=None, params=batches, batch=True
            )  # send request with batch flag
            if response:
                for block_info in response:
                    if "result" in block_info and block_info["result"]:
                        try: # parse into Block object and error handling
                            blocks[block_info["id"] + from_block] = Block(
                                **block_info["result"]
                            )
                        except ValidationError as e:
                            print(
                                f"Error parsing block response for block {block_info['id'] + from_block}: {e}"
                            )

            # wait between batches to respect api rate limit
            if end < to_block + 1:
                time.sleep(1)

        return blocks

