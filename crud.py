# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas

# Orders
def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Orders(customer_name=order.customer_name)
    db.add(db_order)
    db.flush()  # get order_id
    for p in order.products or []:
        db_op = models.OrderProducts(order_id=db_order.order_id, product=p.product, quantity=p.quantity)
        db.add(db_op)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order(db: Session, order_id: int):
    return db.query(models.Orders).filter(models.Orders.order_id == order_id).first()

def list_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Orders).offset(skip).limit(limit).all()

def update_order_customer(db: Session, order_id: int, customer_name: str):
    db_order = get_order(db, order_id)
    if not db_order:
        return None
    db_order.customer_name = customer_name
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = get_order(db, order_id)
    if not db_order:
        return False
    db.delete(db_order)
    db.commit()
    return True

# OrderProducts
def add_or_update_product(db: Session, order_id: int, product_data: schemas.OrderProductCreate):
    db_op = db.query(models.OrderProducts).filter(
        models.OrderProducts.order_id == order_id,
        models.OrderProducts.product == product_data.product
    ).first()
    if db_op:
        db_op.quantity = product_data.quantity
    else:
        db_op = models.OrderProducts(order_id=order_id, product=product_data.product, quantity=product_data.quantity)
        db.add(db_op)
    db.commit()
    return db_op

def delete_product(db: Session, order_id: int, product: str):
    db_op = db.query(models.OrderProducts).filter(
        models.OrderProducts.order_id == order_id,
        models.OrderProducts.product == product
    ).first()
    if not db_op:
        return False
    db.delete(db_op)
    db.commit()
    return True
