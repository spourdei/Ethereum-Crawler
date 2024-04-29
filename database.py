import sqlite3
def create_database():
    # connect and initialize  the SQLite database
    conn = sqlite3.connect('ethereum.db')

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
        value TEXT NOT NULL,
        FOREIGN KEY (blockHash) REFERENCES Blocks(hash) ON DELETE SET NULL
    );
    """

    # execute the SQL commands above
    cursor.execute(create_blocks_table)
    cursor.execute(create_transactions_table)

    # commit and close connection
    conn.commit()
    print("Database and tables successfully created.")
    conn.close()

if __name__ == '__main__':
    create_database()