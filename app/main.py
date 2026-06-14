from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import Base, engine, SessionLocal
from . import models, schemas, crud

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Expense Tracker")


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Smart Expense Tracker API Running"}


@app.post("/expenses")
def add_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db)
):
    return crud.create_expense(db, expense)


@app.get("/expenses")
def list_expenses(
    db: Session = Depends(get_db)
):
    return crud.get_expenses(db)
@app.put("/expenses/{expense_id}")
def update_expense(
    expense_id: int,
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db)
):
    updated_expense = crud.update_expense(
        db,
        expense_id,
        expense
    )

    if not updated_expense:
        return {"error": "Expense not found"}

    return updated_expense


@app.post("/income")
def add_income(
    income: schemas.IncomeCreate,
    db: Session = Depends(get_db)
):
    return crud.create_income(db, income)


@app.get("/income")
def list_income(
    db: Session = Depends(get_db)
):
    return crud.get_income(db)


@app.get("/summary")
def summary(
    db: Session = Depends(get_db)
):
    expenses = crud.get_expenses(db)
    incomes = crud.get_income(db)

    total_expense = sum(e.amount for e in expenses)
    total_income = sum(i.amount for i in incomes)

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense
    }