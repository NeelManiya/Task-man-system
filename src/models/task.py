from database.database import Base
from sqlalchemy import String, Column, Enum, ForeignKey
import enum
from sqlalchemy.orm import relationship


class Task(Base):
    __tablename__ = "task"
    id = Column(String(50), primary_key=True, nullable=False)
    owner_id = Column(String(50), ForeignKey("user.id"))
    title = Column(String(50), nullable=False)
    description = Column(String(50), nullable=False)
    status = Column(String(50), default="pending", nullable=False)

    user = relationship("User", back_populates="task")
