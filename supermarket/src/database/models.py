from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Time, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Branch(Base):
    __tablename__ = 'branches'
    
    id = Column(Integer, primary_key=True)
    branch_code = Column(String, unique=True, nullable=False)
    city = Column(String, nullable=False)
    
    sales = relationship("Sale", back_populates="branch")

class ProductLine(Base):
    __tablename__ = 'product_lines'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    
    products = relationship("Product", back_populates="product_line")

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    product_line_id = Column(Integer, ForeignKey('product_lines.id'), nullable=False)
    unit_price = Column(Float, nullable=False)
    
    product_line = relationship("ProductLine", back_populates="products")
    sales = relationship("Sale", back_populates="product")

class Sale(Base):
    __tablename__ = 'sales'
    
    id = Column(Integer, primary_key=True)
    invoice_id = Column(String, unique=True, nullable=False)
    branch_id = Column(Integer, ForeignKey('branches.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time)
    payment_method = Column(String)
    total = Column(Float, nullable=False)
    tax = Column(Float)
    cogs = Column(Float)
    gross_income = Column(Float)
    rating = Column(Float)
    
    branch = relationship("Branch", back_populates="sales")
    product = relationship("Product", back_populates="sales")
