from decouple import config
from core import DBEngine


#region Variables
DB_USER=config('MYSQL_USER')
DB_PWD=config('MYSQL_PASSWORD')
DB_HOST=config('MYSQL_HOST')
DB_PORT=config('MYSQL_PORT')
DB_NAME=config('MYSQL_DB')
#endregion




if __name__ == '__main__':
    connection_string = f"mysql+mysqlconnector://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    db_engine = DBEngine(connection_string)
    db_engine.get_db_tables()