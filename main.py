# File: app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4, UUID
import uvicorn

app = FastAPI()

# --- Models ---
class Income(BaseModel):
    id: Optional[UUID] = None
    amount: float
    source: str
    description: Optional[str] = None

class Expense(BaseModel):
    id: Optional[UUID] = None
    amount: float
    category: str
    description: Optional[str] = None

class SavingsGoal(BaseModel):
    id: Optional[UUID] = None
    goal_name: str
    target_amount: float
    saved_amount: float = 0.0

class Transaction(BaseModel):
    id: UUID
    type: str  # 'income' or 'expense'
    amount: float
    category: str
    description: Optional[str] = None

# --- Storage ---
income_records: List[Income] = []
expense_records: List[Expense] = []
savings_goals: List[SavingsGoal] = []

# --- Endpoints ---
@app.post("/income/", response_model=Income)
def add_income(income: Income):
    income.id = uuid4()
    income_records.append(income)
    return income

@app.get("/income/", response_model=List[Income])
def get_all_income():
    return income_records

@app.delete("/income/{income_id}")
def delete_income(income_id: UUID):
    global income_records
    income_records = [i for i in income_records if i.id != income_id]
    return {"message": "Income record deleted successfully"}

@app.post("/expenses/", response_model=Expense)
def add_expense(expense: Expense):
    expense.id = uuid4()
    expense_records.append(expense)
    return expense

@app.get("/expenses/", response_model=List[Expense])
def get_all_expenses():
    return expense_records

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: UUID):
    global expense_records
    expense_records = [e for e in expense_records if e.id != expense_id]
    return {"message": "Expense record deleted successfully"}

@app.post("/savings/", response_model=SavingsGoal)
def add_savings_goal(goal: SavingsGoal):
    goal.id = uuid4()
    savings_goals.append(goal)
    return goal

@app.get("/savings/", response_model=List[SavingsGoal])
def get_all_savings_goals():
    return savings_goals

@app.delete("/savings/{goal_id}")
def delete_savings_goal(goal_id: UUID):
    global savings_goals
    savings_goals = [g for g in savings_goals if g.id != goal_id]
    return {"message": "Savings goal deleted successfully"}

@app.get("/transactions/", response_model=List[Transaction])
def get_transactions():
    transactions = [
        Transaction(
            id=i.id, type="income", amount=i.amount, category="Income", description=i.description
        )
        for i in income_records
    ] + [
        Transaction(
            id=e.id, type="expense", amount=e.amount, category=e.category, description=e.description
        )
        for e in expense_records
    ]
    return transactions

@app.get("/balance/")
def calculate_balance():
    total_income = sum(i.amount for i in income_records)
    total_expenses = sum(e.amount for e in expense_records)
    savings_total = sum(g.saved_amount for g in savings_goals)
    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "savings_total": savings_total,
        "current_balance": total_income - total_expenses - savings_total,
    }

# --- Entry point ---
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
