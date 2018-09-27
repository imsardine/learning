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

@pytest.mark.mysql
def test_orm_without_fk_constraints__mysql(mysql_engine):
    conn = mysql_engine.connect()
    trans = conn.begin()
    try:
        conn.execute("CREATE TABLE user (id INT NOT NULL AUTO_INCREMENT, name CHAR(20) NOT NULL, PRIMARY KEY (id));")
        conn.execute("CREATE TABLE address (id INT NOT NULL AUTO_INCREMENT, user_id INT NOT NULL, email_address VARCHAR(50), PRIMARY KEY (id));")
        conn.execute("INSERT INTO user (id, name) VALUES (1, 'Jeremy');")
        conn.execute("INSERT INTO address (id, user_id, email_address) VALUES (1, 1, 'imsardine@gmail.com'), (2, 1, 'jeremykao@kkbox.com')")
        trans.commit()
    except:
        trans.rollback()
        raise

    # Start a new transaction implicitly
    Session = sessionmaker(bind=mysql_engine)
    session = Session()

    try:
        # Test ORM querying
        jeremy = session.query(User).filter_by(id=1).one()
        assert jeremy.name == 'Jeremy'
        assert [addr.email_address for addr in jeremy.addresses] == \
                ['imsardine@gmail.com', 'jeremykao@kkbox.com']

        judy = User(name='Judy')
        judy.addresses.append(Address(email_address='imjudykao@gmail.com'))
        session.add(judy)
        session.commit()

        # Test ORM writing
        judy = session.query(User).filter_by(name='Judy').one()
        assert [addr.email_address for addr in judy.addresses] == ['imjudykao@gmail.com']
        assert judy.addresses[0].user is judy # backref
    finally:
        session.close()

