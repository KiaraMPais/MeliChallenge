from sqlalchemy import create_engine, inspect
from database import sql_connection
from sqlmodel import select
from models import Rule
import re


def load_classification_rules():
    """Cargar las reglas de clasificación desde la base de datos."""
    session = next(sql_connection.get_session())
    try:
        query = session.exec(select(Rule))
        result = query.fetchall()

        rules = {row.rule_name: row.regex_pattern for row in result}
        AnalyzerEngine.classification_rules = rules
    finally:
        session.close()


class AnalyzerEngine:


    """ Reglas de clasificación. Hay que tener en cuenta que no estan como self asi son globales
        Es decir que no hay que hacer una carga por cada instancia de AnalyzerEngine """
    classification_rules = None

    def __init__(self, conn_string=None):
        # Conectarse a la base de datos usando la connection string
        self.connection_string = conn_string
        self.engine = create_engine(self.connection_string)
        if not AnalyzerEngine.classification_rules:
            load_classification_rules()

    def classify_column(self, column_name):
        """Clasifica una columna basándose en su nombre y las reglas predefinidas."""
        for category, regex in self.classification_rules.items():
            if re.search(regex, column_name):
                return category
        return "N/A"

    def classify_db_structure(self):
        """Obtiene y clasifica automáticamente la estructura de la base de datos."""
        # Usar el inspector para obtener las tablas
        inspector = inspect(self.engine)
        # Dict para almacenar la estructura clasificada de la base de datos
        classified_structure = {'tables': {}}

        # Obtener los nombres de todas las tablas en la base de datos
        tables = inspector.get_table_names()

        for table in tables:
            columns = inspector.get_columns(table)
            classified_structure['tables'][table] = []

            for column in columns:
                column_name = column['name']
                column_type = str(column['type'])  # Convertimos el tipo a string para JSON
                classification = self.classify_column(column_name)

                # Almacenar nombre, tipo y clasificación de cada columna
                classified_structure['tables'][table].append({
                    "column_name": column_name,
                    "column_type": column_type,
                    "classification": classification
                })

        return classified_structure