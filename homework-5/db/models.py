from sqlalchemy import Column, Integer, String, Text, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TaskA(Base):
	__tablename__ = 'task_a'
	__table_args__ = {'mysql_charset': 'utf8'}
	id = Column(Integer, primary_key=True, autoincrement=True)
	result = Column(Integer, nullable=False)


class TaskB(Base):
	__tablename__ = 'task_b'
	__table_args__ = {'mysql_charset': 'utf8'}
	id = Column(Integer, primary_key=True, autoincrement=True)
	method = Column(Enum('OPTIONS','GET','HEAD','POST','PUT','DELETE','TRACE','CONNECT'), nullable=False)
	count = Column(Integer, nullable=False)

class TaskC(Base):
	__tablename__ = 'task_c'
	__table_args__ = {'mysql_charset': 'utf8'}
	id = Column(Integer, primary_key=True, autoincrement=True)
	url = Column(Text, nullable=False)
	code = Column(Integer, nullable=False)
	count = Column(Integer, nullable=False)

class TaskD(Base):
	__tablename__ = 'task_d'
	__table_args__ = {'mysql_charset': 'utf8'}
	id = Column(Integer, primary_key=True, autoincrement=True)
	url = Column(Text, nullable=False)
	code = Column(Integer, nullable=False)
	ip = Column(String(15), nullable=False)

class TaskE(Base):
	__tablename__ = 'task_e'
	__table_args__ = {'mysql_charset': 'utf8'}
	id = Column(Integer, primary_key=True, autoincrement=True)
	url = Column(Text, nullable=False)
	code = Column(Integer, nullable=False)
	ip = Column(String(15), nullable=False)
