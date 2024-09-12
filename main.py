from sqlalchemy import create_engine, inspect
from decouple import config


#region Variables
DB_USER=config('MYSQL_USER')
DB_PWD=config('MYSQL_PASSWORD')
DB_HOST=config('MYSQL_HOST')
DB_PORT=config('MYSQL_PORT')
DB_NAME=config('MYSQL_DB')
#endregion


class DBEngine:

    def __init__(self):
        # Conectarse a la base de datos usando la connection string
        self.connection_string = f"mysql+mysqlconnector://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"  # Ejemplo para PostgreSQL
        self.engine = create_engine(self.connection_string)

    def get_db_tables(self):
        # Usar el inspector para obtener las tablas
        inspector = inspect(self.engine)

        db_structure = {}

        # Obtener los nombres de todas las tablas en la base de datos
        tables = inspector.get_table_names()
        db_structure['tables'] = {}

        for table in tables:
            columns = inspector.get_columns(table)
            db_structure['tables'][table] = []

            for column in columns:
                # Almacenar nombre y tipo de cada columna
                db_structure['tables'][table].append({
                    "name": column['name'],
                    "type": str(column['type'])  # Convertimos el tipo a string para JSON
                })
        print(db_structure)


if __name__ == '__main__':
    db_engine = DBEngine()
    db_engine.get_db_tables()