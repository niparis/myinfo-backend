"""
    File for requests schemas.
        Each request should have a schema
        We validate all requests to make sure we can process them.
"""

from typing import List
from pydantic import BaseModel


class GetPersonData(BaseModel):
    code: List[str]
    state: List[str]    
