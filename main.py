# app/main.py
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Orders CRUD API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Orders endpoints
@app.post("/orders/", response_model=schemas.OrderRead, status_code=201)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order)

@app.get("/orders/{order_id}", response_model=schemas.OrderRead)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@app.get("/orders/", response_model=list[schemas.OrderRead])
def list_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_orders(db, skip, limit)

@app.put("/orders/{order_id}", response_model=schemas.OrderRead)
def update_order(order_id: int, payload: schemas.OrderBase, db: Session = Depends(get_db)):
    db_order = crud.update_order_customer(db, order_id, payload.customer_name)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@app.delete("/orders/{order_id}", status_code=204)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_order(db, order_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Order not found")
    return

# OrderProducts endpoints
@app.post("/orders/{order_id}/products", response_model=schemas.OrderProductRead, status_code=201)
def add_product(order_id: int, product: schemas.OrderProductCreate, db: Session = Depends(get_db)):
    if not crud.get_order(db, order_id):
        raise HTTPException(status_code=404, detail="Order not found")
    db_op = crud.add_or_update_product(db, order_id, product)
    return db_op

@app.delete("/orders/{order_id}/products/{product}", status_code=204)
def delete_product(order_id: int, product: str, db: Session = Depends(get_db)):
    ok = crud.delete_product(db, order_id, product)
    if not ok:
        raise HTTPException(status_code=404, detail="Product not found")
    return
