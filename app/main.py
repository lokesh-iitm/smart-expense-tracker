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
@app.delete("/expenses/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db)
):
    deleted_expense = crud.delete_expense(
        db,
        expense_id
    )

    if not deleted_expense:
        return {"error": "Expense not found"}

    return deleted_expense


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
@app.put("/income/{income_id}")
def update_income(
    income_id: int,
    income: schemas.IncomeCreate,
    db: Session = Depends(get_db)
):
    updated_income = crud.update_income(
        db,
        income_id,
        income
    )

    if not updated_income:
        return {"error": "Income not found"}

    return updated_income
@app.delete("/income/{income_id}")
def delete_income(
    income_id: int,
    db: Session = Depends(get_db)
):
    deleted_income = crud.delete_income(
        db,
        income_id
    )

    if not deleted_income:
        return {"error": "Income not found"}

    return deleted_income


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