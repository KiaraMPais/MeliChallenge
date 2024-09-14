from sqlalchemy import create_engine, inspect

class DBEngine:

    def __init__(self, conn_string=None):
        # Conectarse a la base de datos usando la connection string
        self.connection_string = conn_string
        self.engine = create_engine(self.connection_string)



    def get_db_tables(self):

        # Usar el inspector para obtener las tablas
        inspector = inspect(self.engine)
        # Dict temporal para almacenar la estructura de la base de datos
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
