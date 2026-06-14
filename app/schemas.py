
#author :lokesh
from pydantic import BaseModel


class ExpenseCreate(BaseModel):
    title: str
    category: str
    amount: float


class IncomeCreate(BaseModel):
    source: str
    amount: float


class ExpenseResponse(ExpenseCreate):
    id: int

    class Config:
        from_attributes = True


class IncomeResponse(IncomeCreate):
    id: int

    class Config:
        from_attributes = True