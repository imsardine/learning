from tests import *
from textwrap import dedent
import pytest
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    addresses = relationship('Address', order_by='Address.id', back_populates='user')

class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    _user_id = Column('user_id', Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='addresses')

def test_mapping():
    assert create_table_sql(User.__table__, sqlite_dialect) == dedent("""\
        CREATE TABLE user (
        	id INTEGER NOT NULL, 
        	name VARCHAR, 
        	PRIMARY KEY (id)
        )""")

def test_insert():
    user = User(name='Jermey')
    assert user.addresses == []
    email1 = Address(email_address='imsardine@gmail.com')
    assert email1.user is None
    user.addresses.append(email1)
    assert email1.user is user

    email2 = Address(email_address='imsardine@simplbug.com', user=user)
    assert email2 in user.addresses

