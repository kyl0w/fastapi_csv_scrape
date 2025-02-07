from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = 'users'
    
    email = Column(String, primary_key=True, index=True)
    password = Column(String)
    id = Column(String, index=True)
    
class Metadata(Base):
    __tablename__ = "metadata"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    keywords = Column(String, nullable=True)