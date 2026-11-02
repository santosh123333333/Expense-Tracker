from fastapi import FastAPI,Depends,HTTPException,status,APIRouter
from app.core.db import get_db
from app.models.expense import Expense
from app.schemas.apiresponse import APIResponse
from app.schemas.expensesschema import ExpenseCreate,ExpenseResponse
from sqlalchemy.orm import Session





router = APIRouter(
    prefix="/expenses")




#create expense
@router.post("/",response_model=APIResponse)
def create_expense(expense_requestmodel: ExpenseCreate, db: Session = Depends(get_db)):

    # validation if expense is already created and exists in the database
    expenses = db.query(Expense).filter(Expense.title == expense_requestmodel.title).first()
    if expenses:
        raise HTTPException(status_code=400, detail="Expense with this title already exists")


    new_expenses=Expense(
        title=expense_requestmodel.title,
        description=expense_requestmodel.description,
        show=expense_requestmodel.show,
        amount=expense_requestmodel.amount

    )

    db.add(new_expenses)
    db.commit()
    db.refresh(new_expenses)
    print("new_expenses created:"
    )


    return APIResponse(status="success", message="Expense created successfully",
                        data={"expense": ExpenseResponse.model_validate(new_expenses)})

#get all expenses

@router.get("/",response_model=APIResponse)
def get_all_expense(db:Session=Depends(get_db)):
    expenses = db.query(Expense).all()
    return APIResponse(status="success", message="Expenses retrieved successfully",
                        data={"expenses": [ExpenseResponse.model_validate(expense) for expense in expenses]})


#get expense by id
@router.get("/{expense_id}",response_model=APIResponse)
def get_expense_by_id(expense_id: int, db: Session = Depends(get_db)):
    expense=db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return APIResponse(status="success", message="Expense retrieved successfully",
                        data={"expense": ExpenseResponse.model_validate(expense)})

#update expense by id
@router.put("/{expense_id}",response_model=APIResponse)
def update_expense(expense_id: int, expense_requestmodel: ExpenseCreate, db: Session = Depends(get_db)):
    expense=db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    expense.title=expense_requestmodel.title
    expense.description=expense_requestmodel.description
    expense.show=expense_requestmodel.show
    expense.amount=expense_requestmodel.amount
    db.commit()
    db.refresh(expense)
    return APIResponse(status="success", message="Expense updated successfully",
                        data={"expense": ExpenseResponse.model_validate(expense)})



#delete expense by id
@router.delete("/{expense_id}",response_model=APIResponse)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense=db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    return APIResponse(status="success", message="Expense deleted successfully",
                        data={"expense": ExpenseResponse.model_validate(expense)})




#search expenses by title
@router.get("/search/{title}",response_model=APIResponse)
def search_expenses(title: str, db: Session = Depends(get_db)):
    expenses=db.query(Expense).filter(Expense.title.ilike(f"%{title}%")).all()
    if not expenses:
        raise HTTPException(status_code=404, detail="No expenses found with this title")
    return APIResponse(status="success", message="Expenses retrieved successfully",
                        data={"expenses": [ExpenseResponse.model_validate(expense) for expense in expenses]})
