import uuid
from pydantic import BaseModel
from enum import Enum


class SauceSpiciness(str, Enum):
    LEVEL0 = '0'
    LEVEL1 = '1'
    LEVEL2 = '2'
    LEVEL3 = '3'


class SauceBaseSchema(BaseModel):
    name: str
    description: str
    price: float
    spiciness: SauceSpiciness

    class Config:
        orm_mode = True


class SauceCreateSchema(SauceBaseSchema):
    stock: int


class SauceSchema(SauceCreateSchema):
    id: uuid.UUID


class SauceListItemSchema(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    price: float
    spiciness: SauceSpiciness

    class Config:
        orm_mode = True


class SauceUpdateSauceSpicinessSchema(SauceBaseSchema):
    id: uuid.UUID
    spiciness: SauceSpiciness
