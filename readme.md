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


