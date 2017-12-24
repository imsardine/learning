from sqlalchemy.dialects import sqlite, mysql

__all__ = ['sqlite_dialect', 'mysql_dialect', 'create_table_sql', 'sqlite3']

sqlite_dialect = sqlite.dialect()
mysql_dialect = mysql.dialect()

def create_table_sql(table, dialect):
    from sqlalchemy.schema import CreateTable
    return str(CreateTable(table).compile(dialect=dialect)).strip()

def sqlite3(db_file, command):
    import subprocess
    return subprocess.check_output(['sqlite3', db_file, command])

