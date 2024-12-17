from pydantic import BaseModel
from enum import Enum
from typing import Optional

class AudienceType(str, Enum):
    AGE_RANGE = "age_range"
    GENDER = "gender"
    OTHER = "other"

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"

class GroupClassification(BaseModel):
    audience_type: AudienceType
    split_recommended: bool
    age_start: Optional[int]
    age_end: Optional[int]
    gender: Optional[Gender]