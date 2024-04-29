--  This is the schema for the database with Blocks and Transactions tables.

-- Create Blocks table
CREATE TABLE IF NOT EXISTS Blocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hash TEXT NOT NULL UNIQUE,
    number TEXT NOT NULL UNIQUE,
    timestamp TEXT NOT NULL
);

-- Create Transactions table
CREATE TABLE IF NOT EXISTS Transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hash TEXT NOT NULL UNIQUE,
    blockHash TEXT,
    blockNumber TEXT,
    from_ TEXT NOT NULL,
    "to" TEXT,
    value DECIMAL(30, 18), -- for precision
    FOREIGN KEY (blockNumber) REFERENCES Blocks(number) ON DELETE SET NULL
);