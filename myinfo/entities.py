"""
    File for business entities - allows to cleanly separate business logic from data access layer
"""

from logging import basicConfig
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum, auto



class Person(BaseModel):
    uinfin: dict
    name: dict
    sex: dict
    race: dict
    nationality: dict
    dob: dict
    email: dict
    mobileno: dict
    regadd: dict
    housingtype: dict
    hdbtype: dict
    marital: dict
    edulevel: dict
    noa_basic: dict = Field(alias='noa-basic')
    ownerprivate: dict
    cpfcontributions: dict
    cpfbalances: dict


