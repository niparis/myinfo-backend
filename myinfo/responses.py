"""
    File for responses schemas.
        We have a few generic schemas.
        The goal is to make sure that there's no surprise from the front-end on the structure of the responses
        As the backend grows, there might be some non-generic responses
"""

from typing import Any, Optional
from pydantic import BaseModel
from enum import Enum, auto

from myinfo.entities import Person


class GenericResponse(BaseModel):
    msg: Optional[str]
    data: Any


class GenericErrorResponse(BaseModel):
    msg: str
    details: Optional[str]


class PersonResponse(GenericResponse):
    data: Person
