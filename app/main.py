from fastapi import FastAPI
from app.core.db import engine,Base

from app.router import expenses, userss


app = FastAPI()


#create tables
Base.metadata.create_all(bind=engine)


#include routers


app.include_router(userss.router)
app.include_router(expenses.router)


@app.get("/")
def root():
    return {"message": "Hello, World!"}