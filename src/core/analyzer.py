import random
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError
from database import sql_connection
from sqlmodel import select
from models import Rule
import re


def load_classification_rules():
    """Cargar las reglas de clasificación desde la base de datos."""
    session = next(sql_connection.get_session())
    try:
        field_rules = session.exec(select(Rule).where(Rule.is_value_rule == False))
        result = field_rules.fetchall()
        AnalyzerEngine.field_rules = {row.rule_name: row.regex_pattern for row in result}

        value_rules = session.exec(select(Rule).where(Rule.is_value_rule == True))
        result = value_rules.fetchall()
        AnalyzerEngine.value_rules = {row.rule_name: row.regex_pattern for row in result}

    finally:
        session.close()


class AnalyzerEngine:
    field_rules = None
    value_rules = None

    def __init__(self, conn_string=None):
        self.connection_string = conn_string
        self.engine = create_engine(self.connection_string)
        if not AnalyzerEngine.field_rules or not AnalyzerEngine.value_rules:
            load_classification_rules()

    def classify_column(self, column_name):
        """Clasifica una columna basándose en su nombre y las reglas predefinidas."""
        for category, regex in self.field_rules.items():
            if re.search(regex, column_name):
                return category
        return "N/A"

    def classify_column_by_data(self, table, column_name):
        """Clasifica una columna basada en una muestra aleatoria de sus datos."""
        try:
            with self.engine.connect() as connection:
                # Obtener la cuenta total de filas en la tabla
                total_rows = connection.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()

                # Si no hay filas, devolver "N/A"
                if total_rows == 0:
                    print(f"La tabla '{table}' no contiene filas.")
                    return "N/A"

                # Seleccionar el número adecuado de filas (máximo 10, o menos si no hay suficientes)
                num_rows_to_fetch = min(10, total_rows)

                # Seleccionar índices aleatorios y obtener las filas
                random_offsets = random.sample(range(total_rows), num_rows_to_fetch)
                data_sample = []
                for offset in random_offsets:
                    result = connection.execute(text(f"SELECT {column_name} FROM {table} LIMIT 1 OFFSET {offset}"))
                    data_sample.append(result.fetchone())

            # Clasificar los datos obtenidos usando las reglas basadas en patrones de valores
            classifications = []
            for category, pattern in self.value_rules.items():
                for row in data_sample:
                    if row and row[0] is not None:  # Verificar que la fila no sea nula
                        value = str(row[0])
                        if re.match(pattern, value):
                            classifications.append(category)
                            break  # Si hay coincidencia, romper el loop interno

            # Si no se encontró ninguna coincidencia, devolver "N/A"
            return classifications[0] if classifications else "N/A"

        except SQLAlchemyError as e:
            # Manejo de errores relacionados con la base de datos
            print(f"Error en la consulta SQL: {str(e)}")
            return "N/A"
        except Exception as e:
            # Manejo de otros errores inesperados
            print(f"Error clasificando los datos de la columna '{column_name}' en la tabla '{table}': {str(e)}")
            return "N/A"

    def classify_db_structure(self):
        """Obtiene y clasifica automáticamente la estructura de la base de datos."""
        try:
            inspector = inspect(self.engine)
            classified_structure = {'tables': {}}
            tables = inspector.get_table_names()

            for table in tables:
                columns = inspector.get_columns(table)
                classified_structure['tables'][table] = []

                for column in columns:
                    column_name = column['name']
                    column_type = str(column['type'])
                    # Clasificar los valores en funcion del nombre de la columna
                    classification_by_name = self.classify_column(column_name)
                    # Clasificar también los datos de la columna
                    value_classification = self.classify_column_by_data(table, column_name)

                    classified_structure['tables'][table].append({
                        "column_name": column_name,
                        "column_type": column_type,
                        "classification_by_name": classification_by_name,
                        "classification_by_data": value_classification
                    })

            return classified_structure

        except SQLAlchemyError as e:
            print(f"Error al inspeccionar la base de datos: {str(e)}")
            return None
        except Exception as e:
            print(f"Error clasificando la estructura de la base de datos: {str(e)}")
            return None
