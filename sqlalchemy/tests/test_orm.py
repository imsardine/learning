from tests import *
from textwrap import dedent
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

def test_mapping_process():
    # Instrumented
    assert isinstance(User.id, sqlalchemy.orm.attributes.InstrumentedAttribute)

    # Mappped
    assert Base.metadata == User.__table__.metadata
    assert Base.metadata.tables == { 'user': User.__table__ }
    assert create_table_sql(User.__table__, sqlite_dialect) == dedent("""\
        CREATE TABLE user (
        	id INTEGER NOT NULL, 
        	name VARCHAR, 
        	fullname VARCHAR, 
        	PRIMARY KEY (id)
        )""")

