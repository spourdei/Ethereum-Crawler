import sys
from api import EthereumAPI
from constants import endpoint_url
from database import create_database, connect_database, populate_database


def main():
    create_database("ethereum.db")
    connection = connect_database("ethereum.db")

    if len(sys.argv) == 3:  # check for system args
        from_block = int(sys.argv[1])
        to_block = int(sys.argv[2])

        # create an instance of EthereumAPI
        ethereum_api = EthereumAPI(endpoint_url)

        print(f"Fetching blocks from {from_block} to {to_block}")
        blocks = ethereum_api.get_blocks_in_batch(from_block, to_block)
        print("Populating database...")
        populate_database(connection, blocks)
        print("Successfully finished populating database.")

    else:
        print(
            "Invalid arguments. Try again. Correct usage: python database.py <from_block> <to_block>"
        )


if __name__ == "__main__":
    main()
