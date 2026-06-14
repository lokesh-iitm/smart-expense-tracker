#author : lokesh

from pydantic import BaseModel, Field
from datetime import date   


class ExpenseCreate(BaseModel):
    title: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)
    date: date



class IncomeCreate(BaseModel):
    source: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)


class ExpenseResponse(ExpenseCreate):
    id: int

    class Config:
        from_attributes = True


class IncomeResponse(IncomeCreate):
    id: int

    class Config:
        from_attributes = True