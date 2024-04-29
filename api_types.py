from pydantic import BaseModel, Field
from typing import List, Optional

#create data model for Transaction object based on only necessary fields
class Transaction(BaseModel):
    hash: str
    blockHash: Optional[str] = None  # optional since it can be None for pending transactions
    blockNumber: Optional[str] = None
    from_: str = Field(alias='from')  # using alias to handle conflict with "from" for Python
    to: Optional[str] = None  # optional, as it could be None when its a contract creation transaction
    value: str

#create data model for Block object based on only necessary fields
class Block(BaseModel):
    hash: str
    number: str
    timestamp: str
    transactions: List[Transaction] # list of transactions involved in each block

class BlockResponse(BaseModel):
    result: str

class GetBlockByNumberResponse(BaseModel):
    result: Optional[Block]