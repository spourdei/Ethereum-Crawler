# Ethereum Block Crawler
This is an Ethereum block crawler that retrieves Ethereum Mainnet transactions within a given block 
range and populates a database with it.


## Getting Started

To get started please make sure you have python 3.11 and poetry installed. Run the following:

```
poetry install
```

Create the .env file in the project directory and replace the endpoint_url with your url. It will look like: 

```
ENDPOINT_URL=https://your_endpoint_here
```

We then need to create and initialize a database first. We can do this by running
```
poetry run python populate_database.py from_block to_block
```

For example, if we are looking for the range from block 18908800 to 18909050:
```
poetry run python populate_database.py 18908800 18909050
```

This will create an instance of "ethereum.db" and populate it with the respective block and transactions data.


## Block with highest value of eth transferred

We can find the block with the most eth transferred by running

```
poetry run python block_finder.py
```

This will return the result as well as saving it to a file result.txt.

## Future steps 

1. For the sake of this challenge, I made the decision to hardcode 2 values into this project in order to comply with
the project outline for script 2. A beneficial change for block_finder.py would be to modify the script to accept two system arguments 
representing the datetime values for the start and end of the range. This change would allow dynamic specification 
of the block timestamps, rather than embedding fixed values directly in the SQL query as such:

```Blocks.timestamp BETWEEN '2024-01-01 00:00:00' AND '2024-01-01 00:30:00'```

2. For this project, I opted for SQLite over PostgreSQL for several key reasons:

* Simplicity: SQLite is a file-based database that does not require a separate server to run. 
* Ease of Setup: This ease of setup is particularly advantageous for this project that needs to be quickly deployable and easily maintainable.
* Portability: Being file-based, it makes sharing this project much simpler and easier.

If this project was to be scalable, I would have opted for PostgreSQL instead.