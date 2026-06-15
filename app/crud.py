#author : lokesh

from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy import or_


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


def get_expenses(
    db: Session,
    page: int = 1,
    limit: int = 5
):
    skip = (page - 1) * limit

    return (
        db.query(models.Expense)
        .offset(skip)
        .limit(limit)
        .all()
    )
def get_expenses_sorted_by_amount(
    db: Session
):
    return (
        db.query(models.Expense)
        .order_by(models.Expense.amount.desc())
        .all()
    )
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
        .filter(
            or_(
                models.Expense.title.contains(keyword),
                models.Expense.category.contains(keyword)
            )
        )
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
def get_date_range_report(
    db: Session,
    start_date,
    end_date
):
    expenses = (
        db.query(models.Expense)
        .filter(models.Expense.date >= start_date)
        .filter(models.Expense.date <= end_date)
        .all()
    )

    total_expense = sum(
        expense.amount
        for expense in expenses
    )

    return {
        "start_date": start_date,
        "end_date": end_date,
        "total_expense": total_expense,
        "total_transactions": len(expenses)
    }
def get_top_categories(db: Session):
    expenses = db.query(models.Expense).all()

    category_totals = {}

    for expense in expenses:
        if expense.category not in category_totals:
            category_totals[expense.category] = 0

        category_totals[expense.category] += expense.amount

    result = []

    for category, total in category_totals.items():
        result.append({
            "category": category,
            "total_spent": total
        })

    result.sort(
        key=lambda x: x["total_spent"],
        reverse=True
    )

    return result
def get_dashboard_data(
    db: Session
):
    expenses = db.query(models.Expense).all()
    incomes = db.query(models.Income).all()

    total_expense = sum(
        expense.amount
        for expense in expenses
    )

    total_income = sum(
        income.amount
        for income in incomes
    )

    category_totals = {}

    for expense in expenses:
        if expense.category not in category_totals:
            category_totals[expense.category] = 0

        category_totals[expense.category] += expense.amount

    top_category = None

    if category_totals:
        top_category = max(
            category_totals,
            key=category_totals.get
        )

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense,
        "total_transactions": len(expenses),
        "top_category": top_category
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
    db_expense.date = expense.date
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