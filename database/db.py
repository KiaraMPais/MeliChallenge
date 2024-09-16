from sqlmodel import SQLModel, Session, create_engine
from decouple import config
from contextlib import contextmanager


class SQLConnection:
    def __init__(self):
        connection_string = (f"mysql+mysqlconnector://{config('MYSQL_USER')}:{config('MYSQL_PASSWORD')}@"
                             f"{config('MYSQL_HOST')}:{config('MYSQL_PORT')}/{config('MYSQL_DB')}")

        self.engine = create_engine(connection_string, echo=True)


    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)


    def get_session(self):
        with Session(self.engine) as session:
            yield session

sql_connection = SQLConnection()
