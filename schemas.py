# app/schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional

class OrderProductBase(BaseModel):
    product: str = Field(..., example="Mouse")
    quantity: int = Field(..., ge=0, example=1)

class OrderProductCreate(OrderProductBase):
    pass

class OrderProductRead(OrderProductBase):
    order_id: int

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    customer_name: str = Field(..., example="John Doe")

class OrderCreate(OrderBase):
    products: Optional[List[OrderProductCreate]] = []

class OrderRead(OrderBase):
    order_id: int
    products: List[OrderProductRead] = []

    class Config:
        orm_mode = True
