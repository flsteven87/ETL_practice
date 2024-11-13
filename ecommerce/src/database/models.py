from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    
    customer_id = Column(Integer, primary_key=True)
    customer_since = Column(String(20))
    orders = relationship("Order", back_populates="customer")

class Category(Base):
    __tablename__ = 'categories'
    
    category_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = 'products'
    
    product_id = Column(Integer, primary_key=True)
    sku = Column(String(100), unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.category_id'))
    price = Column(Float, nullable=False)
    
    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")

class Order(Base):
    __tablename__ = 'orders'
    
    order_id = Column(Integer, primary_key=True)
    increment_id = Column(String(20))
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    status = Column(String(20))
    created_at = Column(String(20))
    payment_method = Column(String(50))
    grand_total = Column(Float)
    discount_amount = Column(Float, default=0)
    sales_commission_code = Column(String(20))
    bi_status = Column(String(20))
    
    customer = relationship("Customer", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = 'order_items'
    
    order_item_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'))
    product_id = Column(Integer, ForeignKey('products.product_id'))
    qty_ordered = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")