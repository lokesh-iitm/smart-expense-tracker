from sqlalchemy.orm import Session
from . import models, schemas


def create_expense(db: Session, expense: schemas.ExpenseCreate):
    db_expense = models.Expense(
        title=expense.title,
        category=expense.category,
        amount=expense.amount
    )

    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    return db_expense


def get_expenses(db: Session):
    return db.query(models.Expense).all()


def create_income(db: Session, income: schemas.IncomeCreate):
    db_income = models.Income(
        source=income.source,
        amount=income.amount
    )

    db.add(db_income)
    db.commit()
    db.refresh(db_income)

    return db_income


def get_income(db: Session):
    return db.query(models.Income).all()