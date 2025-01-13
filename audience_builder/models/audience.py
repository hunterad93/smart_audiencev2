from pydantic import BaseModel
from enum import Enum
from typing import Optional

class DataGroupDefinition(BaseModel):
    description: str
    name: str

class AudienceStructure(BaseModel):
    audience_name: str
    data_groups: list[DataGroupDefinition]