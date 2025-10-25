# app/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from .database import Base

class Orders(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)

    products = relationship("OrderProducts", back_populates="order", cascade="all, delete-orphan")

class OrderProducts(Base):
    __tablename__ = "order_products"
    order_id = Column(Integer, ForeignKey("orders.order_id", ondelete="CASCADE"), nullable=False)
    product = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    __table_args__ = (PrimaryKeyConstraint("order_id", "product", name="pk_order_product"),)

    order = relationship("Orders", back_populates="products")
