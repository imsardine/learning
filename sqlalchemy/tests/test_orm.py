from tests import *
from textwrap import dedent
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import inspect

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

def test_create_session_factory():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine('sqlite:///:memory:')
    Session = sessionmaker(bind=engine) # factory
    assert not isinstance(Session, sqlalchemy.orm.Session)

    session = Session() # instantiation
    assert isinstance(session, sqlalchemy.orm.Session)

def test_insert(caplog):
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()

    user = User(name='Jeremy', fullname='Jeremy Kao')
    assert user not in session
    assert inspect(user).transient

    session.add(user)
    assert inspect(user).pending
    assert user.id == None

    caplog.clear()
    session.commit()

    sqls = [r.message for r in caplog.records]
    assert inspect(user).persistent
    assert user.id == 1
    assert sqls == [
        'BEGIN (implicit)',
        'INSERT INTO user (name, fullname) VALUES (?, ?)',
        "('Jeremy', 'Jeremy Kao')",
        'COMMIT'
    ]

