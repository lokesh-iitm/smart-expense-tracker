from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from .database import Base, engine, SessionLocal
from . import models, schemas, crud
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Expense Tracker")
templates = Jinja2Templates(directory="templates")
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )

@app.post("/expenses")
def add_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db)
):
    return crud.create_expense(db, expense)


@app.get("/expenses")
def list_expenses(
    page: int = 1,
    limit: int = 5,
    db: Session = Depends(get_db)
):
    return crud.get_expenses(
        db,
        page,
        limit
    )
@app.get("/expenses/sort/amount")
def sort_expenses_by_amount(
    db: Session = Depends(get_db)
):
    return crud.get_expenses_sorted_by_amount(
        db
    )
@app.get("/expenses/category/{category}")
def expenses_by_category(
    category: str,
    db: Session = Depends(get_db)
):
    return crud.get_expenses_by_category(
        db,
        category
    )
@app.get("/expenses/search/{keyword}")
def search_expenses(
    keyword: str,
    db: Session = Depends(get_db)
):
    return crud.search_expenses(
        db,
        keyword
    )
@app.get("/reports/monthly/{month}")
def monthly_report(
    month: str,
    db: Session = Depends(get_db)
):
    return crud.get_monthly_report(
        db,
        month
    )
@app.get("/reports/range/{start_date}/{end_date}")
def date_range_report(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db)
):
    return crud.get_date_range_report(
        db,
        start_date,
        end_date
    )
@app.get("/analytics/top-categories")
def top_categories(
    db: Session = Depends(get_db)
):
    return crud.get_top_categories(db)
@app.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db)
):
    return crud.get_dashboard_data(
        db
    )
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
        raise HTTPException(
        status_code=404,
        detail="Expense not found"
    )
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
         raise HTTPException(
        status_code=404,
        detail="Expense not found"
    )
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
        raise HTTPException(
        status_code=404,
        detail="Income not found"
    )
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
        raise HTTPException(
        status_code=404,
        detail="Income not found"
    )

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