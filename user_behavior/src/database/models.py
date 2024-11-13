from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Time, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    behavior_data = relationship("UserBehavior", back_populates="user")

class Device(Base):
    __tablename__ = 'devices'

    device_id = Column(Integer, primary_key=True, autoincrement=True)
    device_model = Column(String, nullable=False)
    behavior_data = relationship("UserBehavior", back_populates="device")

class OS(Base):
    __tablename__ = 'os'

    os_id = Column(Integer, primary_key=True, autoincrement=True)
    operating_system = Column(String, nullable=False)
    behavior_data = relationship("UserBehavior", back_populates="os")

class UserBehavior(Base):
    __tablename__ = 'user_behaviors'

    behavior_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    device_id = Column(Integer, ForeignKey('devices.device_id'), nullable=False)
    os_id = Column(Integer, ForeignKey('os.os_id'), nullable=False)
    
    app_usage_time = Column(Float, nullable=False)
    screen_on_time = Column(Float, nullable=False)
    battery_drain = Column(Float, nullable=False)
    num_apps_installed = Column(Integer, nullable=False)
    data_usage = Column(Float, nullable=False)
    behavior_class = Column(Integer, nullable=False)

    user = relationship("User", back_populates="behavior_data")
    device = relationship("Device", back_populates="behavior_data")
    os = relationship("OS", back_populates="behavior_data")

