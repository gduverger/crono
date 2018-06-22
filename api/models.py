from apistar_sqlalchemy import database
from sqlalchemy import Column, Integer, String

class PuppyModel(database.Base):
	__tablename__ = "Puppy"
	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String)
