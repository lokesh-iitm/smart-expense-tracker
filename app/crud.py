#author : lokesh

from sqlalchemy.orm import Session
from . import models, schemas


def create_expense(db: Session, expense: schemas.ExpenseCreate):
    db_expense = models.Expense(
        title=expense.title,
        category=expense.category,
        amount=expense.amount,
        date=expense.date
    )

    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    return db_expense


def get_expenses(db: Session):
    return db.query(models.Expense).all()
def get_expenses_by_category(
    db: Session,
    category: str
):
    return (
        db.query(models.Expense)
        .filter(models.Expense.category == category)
        .all()
    )
def search_expenses(
    db: Session,
    keyword: str
):
    return (
        db.query(models.Expense)
        .filter(models.Expense.title.contains(keyword))
        .all()
    )
def get_monthly_report(
    db: Session,
    month: str
):
    expenses = db.query(models.Expense).all()

    monthly_expenses = [
        expense
        for expense in expenses
        if str(expense.date).startswith(month)
    ]

    total_expense = sum(
        expense.amount
        for expense in monthly_expenses
    )

    return {
        "month": month,
        "total_expense": total_expense,
        "total_transactions": len(monthly_expenses)
    }


def update_expense(
    db: Session,
    expense_id: int,
    expense: schemas.ExpenseCreate
):
    db_expense = (
        db.query(models.Expense)
        .filter(models.Expense.id == expense_id)
        .first()
    )

    if not db_expense:
        return None

    db_expense.title = expense.title
    db_expense.category = expense.category
    db_expense.amount = expense.amount

    db.commit()
    db.refresh(db_expense)

    return db_expense


def delete_expense(
    db: Session,
    expense_id: int
):
    db_expense = (
        db.query(models.Expense)
        .filter(models.Expense.id == expense_id)
        .first()
    )

    if not db_expense:
        return None

    db.delete(db_expense)
    db.commit()

    return {"message": "Expense deleted successfully"}


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


def update_income(
    db: Session,
    income_id: int,
    income: schemas.IncomeCreate
):
    db_income = (
        db.query(models.Income)
        .filter(models.Income.id == income_id)
        .first()
    )

    if not db_income:
        return None

    db_income.source = income.source
    db_income.amount = income.amount

    db.commit()
    db.refresh(db_income)

    return db_income


def delete_income(
    db: Session,
    income_id: int
):
    db_income = (
        db.query(models.Income)
        .filter(models.Income.id == income_id)
        .first()
    )

    if not db_income:
        return None

    db.delete(db_income)
    db.commit()

    return {"message": "Income deleted successfully"}