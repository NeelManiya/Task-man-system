from database.database import Base
from sqlalchemy import String, Column, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"
    id = Column(String(50), primary_key=True, nullable=False)
    username = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)

    task = relationship("Task", back_populates="user")


class OTP(Base):
    __tablename__ = "otp"
    id = Column(String(100), primary_key=True, nullable=False)
    user_id = Column(String(100), ForeignKey("user.id"), nullable=False)
    email = Column(String(100), nullable=False)
    otp = Column(String(100), nullable=False)
