from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
import re


# Mueve la definición de DatabaseConnection antes de su uso
class DatabaseConnection(BaseModel):
    host: str
    port: int
    username: str
    password: str


class CreateTableModel(BaseModel):
    database_name: str
    table_name: str
    columns: dict  # Ejemplo: {"column1": "VARCHAR(255)", "column2": "INT"}


class CreateDatabaseModel(BaseModel):
    database_name: str


class DatabaseClassifierAPI:
    def __init__(self):
        self.app = FastAPI()
        self.connections = {}
        self.patterns = {
            "FIRST_NAME": r"first_name",
            "LAST_NAME": r"last_name",
            "EMAIL_ADDRESS": r"email",
            "CREDIT_CARD_NUMBER": r"credit_card"
        }
        self.setup_routes()

    def setup_routes(self):
        @self.app.post("/api/v1/database")
        def add_database(connection: DatabaseConnection):
            return self.add_database_connection(connection)

        @self.app.post("/api/v1/database/scan/{id}")
        def scan_database(id: int):
            return self.scan_database_by_id(id)

        @self.app.get("/api/v1/database/scan/{id}")
        def get_scan_result(id: int):
            return self.get_scan_result_by_id(id)

        # Endpoint para ver todas las bases de datos
        @self.app.get("/api/v1/databases/{id}")
        def list_databases(id: int):
            return self.list_databases(id)

    def add_database_connection(self, connection: DatabaseConnection):
        try:
            conn = mysql.connector.connect(
                host=connection.host,
                port=connection.port,
                user=connection.username,
                password=connection.password
            )
            conn.close()
            db_id = len(self.connections) + 1
            connection_data = {
                "host": connection.host,
                "port": connection.port,
                "username": connection.username,
                "password": connection.password,
                "database_name": "test_db"  # Inicialmente sin base de datos, hasta que se cree
            }
            self.connections[db_id] = connection_data
            return {"id": db_id}
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))

    def scan_database_by_id(self, id: int):
        if id not in self.connections:
            raise HTTPException(status_code=404, detail="Database not found")

        connection = self.connections[id]
        try:
            # Acceder al nombre de la base de datos desde el diccionario
            database_name = connection["database_name"]
            conn = mysql.connector.connect(
                host=connection["host"],
                port=connection["port"],
                user=connection["username"],
                password=connection["password"],
                database=database_name  # Selecciona la base de datos correctamente
            )
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()

            result = {}
            for (table,) in tables:
                cursor.execute(f"DESCRIBE {table}")
                columns = cursor.fetchall()
                result[table] = []
                for column in columns:
                    column_name = column[0]
                    col_class = "N/A"
                    for info_type, pattern in self.patterns.items():
                        if re.search(pattern, column_name.lower()):
                            col_class = info_type
                            break
                    result[table].append({"column": column_name, "information_type": col_class})

            conn.close()
            return result
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))

    def get_scan_result_by_id(self, id: int):
        if id not in self.connections:
            raise HTTPException(status_code=404, detail="Database not found")
        return {"message": "Scan result will be here"}

    def list_databases(self, id: int):
        if id not in self.connections:
            raise HTTPException(status_code=404, detail="Database not found")

        connection = self.connections[id]
        try:
            conn = mysql.connector.connect(
                host=connection.host,
                port=connection.port,
                user=connection.username,
                password=connection.password
            )
            cursor = conn.cursor()
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            conn.close()
            return {"databases": [db[0] for db in databases]}
        except mysql.connector.Error as err:
            raise HTTPException(status_code=500, detail=str(err))


# Crear una instancia de la API
db_classifier_api = DatabaseClassifierAPI()

# Ejecutar FastAPI
app = db_classifier_api.app
