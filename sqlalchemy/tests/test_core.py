from tests import *
from os import path
from textwrap import dedent
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

def test_lazy_connecting(tmpdir):
    db_file = path.join(tmpdir.strpath, 'test.db')
    engine = create_engine('sqlite:///%s' % db_file) # Database URL
    assert isinstance(engine, sqlalchemy.engine.Engine)
    assert not path.exists(db_file) # lazy connecting

    conn = engine.connect()
    assert isinstance(conn, sqlalchemy.engine.Connection)
    assert path.exists(db_file)

def test_define_tables_sqlite():
    metadata = MetaData()
    users = Table('user', metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String),
            Column('fullname', String),
    )
    addresses = Table('address', metadata,
            Column('id', Integer, primary_key=True),
            Column('user_id', None, ForeignKey('user.id')),
            Column('email', String, nullable=False),
    )

    assert create_table_sql(users, sqlite_dialect) == dedent("""\
        CREATE TABLE user (
        	id INTEGER NOT NULL, 
        	name VARCHAR, 
        	fullname VARCHAR, 
        	PRIMARY KEY (id)
        )""")

    assert create_table_sql(addresses, sqlite_dialect) == dedent("""\
        CREATE TABLE address (
        	id INTEGER NOT NULL, 
        	user_id INTEGER, 
        	email VARCHAR NOT NULL, 
        	PRIMARY KEY (id), 
        	FOREIGN KEY(user_id) REFERENCES user (id)
        )""")

def test_define_tables_mysql():
    # CompileError: (in table 'user', column 'name'): VARCHAR requires a length on dialect mysql
    metadata = MetaData()
    users = Table('user', metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String(20)),
            Column('fullname', String(50)),
    )
    addresses = Table('address', metadata,
            Column('id', Integer, primary_key=True),
            Column('user_id', None, ForeignKey('user.id')),
            Column('email', String(100), nullable=False),
    )

    assert create_table_sql(users, mysql_dialect) == dedent("""\
        CREATE TABLE user (
        	id INTEGER NOT NULL AUTO_INCREMENT, 
        	name VARCHAR(20), 
        	fullname VARCHAR(50), 
        	PRIMARY KEY (id)
        )""")

    assert create_table_sql(addresses, mysql_dialect) == dedent("""\
        CREATE TABLE address (
        	id INTEGER NOT NULL AUTO_INCREMENT, 
        	user_id INTEGER, 
        	email VARCHAR(100) NOT NULL, 
        	PRIMARY KEY (id), 
        	FOREIGN KEY(user_id) REFERENCES user (id)
        )""")

def test_create_tables(tmpdir):
    db_file = path.join(tmpdir.strpath, 'test.db')

    engine = create_engine('sqlite:///%s' % db_file)
    metadata = MetaData()
    users = Table('user', metadata, Column('id', Integer, primary_key=True))

    metadata.create_all(engine)
    assert sqlite3(db_file, '.schema'), dedent("""\
        CREATE TABLE user (
        	id INTEGER NOT NULL,
        	PRIMARY KEY (id)
        );""")

