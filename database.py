import sqlite3
import sys
from api import EthereumAPI
from sqlite3 import Error
from constants import endpoint_url
from helpers import format_timestamp, convert_wei_to_ether


def connect_database(db):
    """create a database connection to a SQLite database"""
    connection = None
    try:
        connection = sqlite3.connect(db)
        print(f"SQLite Database connected to successfully.")
    except Error as e:
        print(e)
    return connection


def create_database(db):
    """
    create and initialize the SQLite database
    """
    conn = sqlite3.connect(db)

    # create a cursor object
    cursor = conn.cursor()

    # SQL commands to create two tables based on Block and Transaction objects in api_types.py
    create_blocks_table = """
    CREATE TABLE IF NOT EXISTS Blocks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hash TEXT NOT NULL UNIQUE,
        number TEXT NOT NULL UNIQUE,
        timestamp TEXT NOT NULL
    );
    """

    create_transactions_table = """
    CREATE TABLE IF NOT EXISTS Transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hash TEXT NOT NULL UNIQUE,
    blockHash TEXT,
    blockNumber TEXT,
    from_ TEXT NOT NULL,
    "to" TEXT,
    value DECIMAL(30, 18),
    FOREIGN KEY (blockNumber) REFERENCES Blocks(number) ON DELETE SET NULL
    );
    """

    # execute the SQL commands above
    cursor.execute(create_blocks_table)
    cursor.execute(create_transactions_table)

    # commit and close connection
    conn.commit()
    print("Database and tables successfully created.")
    conn.close()


def populate_database(connection, blocks):
    """
    inserts blocks and transactions data within the given range into the database
    """

    # establish connection and cursor
    cursor = connection.cursor()
    for block_number, block in blocks.items():  # insert block data into Blocks table
        parsed_timestamp = format_timestamp(block.timestamp)
        current_values = (block.hash, block.number, parsed_timestamp)

        cursor.execute(
            "INSERT INTO Blocks (hash, number, timestamp) VALUES (?, ?, ?)",
            current_values,
        )
        # insert transactions data into Transactions table
        for transaction in block.transactions:
            converted_value = convert_wei_to_ether(
                transaction.value
            )  # convert transaction value from wei to ether
            transaction_values = (
                transaction.hash,
                block.hash,
                block.number,
                transaction.from_,
                transaction.to,
                converted_value,
            )
            cursor.execute(  # handle conflict with SQL "to"
                'INSERT INTO Transactions (hash, blockHash, blockNumber, from_, "to", value) VALUES (?, ?, ?, ?, ?, ?)',
                transaction_values,
            )

    connection.commit()


def get_largest_block(db):
    """
    executes sql query to find the block with the largest volume of eth transferred and
    returns the block number and value
    """
    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    # SQL query to find the block with the most volume transferred
    query = """
    SELECT 
        Blocks.number AS BlockNumber,
        SUM(CAST(Transactions.value AS REAL)) AS TotalVolume  -- Cast to real for summing
    FROM 
        Blocks
    JOIN 
        Transactions ON Blocks.number = Transactions.blockNumber
    WHERE 
        Blocks.timestamp BETWEEN '2024-01-01 00:00:00' AND '2024-01-01 00:30:00'
    GROUP BY 
        Blocks.number
    ORDER BY 
        TotalVolume DESC
    LIMIT 1;
    """
    cursor.execute(query)

    # grab result & close db
    result = cursor.fetchone()

    connection.close()

    if result:
        return {
            "Block Number": int(result[0], 16),  # convert to int and return result
            "Total Volume Transferred": result[1],
        }
    else:
        return "No result found."


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
