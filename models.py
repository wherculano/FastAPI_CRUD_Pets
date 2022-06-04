from sqlalchemy import String, Column, Integer

from database import Base


class Pet(Base):
    """ Class relationed to Database """
    __tablename__ = 'pets'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=15), nullable=False)
    kind = Column(String, nullable=True)
    breed = Column(String, nullable=True)