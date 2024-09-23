# Challenge para Mercado Libre - Data Sec

## Descripción del Proyecto

Esta aplicación fue sido desarrollada como parte de un challenge para Mercado Libre - Data Sec. Su objetivo es identificar y clasificar datos sensibles almacenados en bases de datos, como nombres, direcciones de correo electrónico, direcciones IP, números de tarjetas de crédito, entre otros. La aplicación es extensible, lo que permite agregar nuevos tipos de información sensible mediante el uso de expresiones regulares y una base de datos para almacenar las reglas de clasificación.

## Instalación y Configuración

### Requisitos

- Python 3.8 o superior
- MySQL o cualquier motor de base de datos compatible con SQLAlchemy
- Docker (opcional)

### Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/KiaraMPais/MeliChallenge.git
   cd MeliChallenge
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Configura las variables de entorno (ver sección de Variables de entorno más abajo).

4. Ejecuta la aplicación:
   ```bash
   python main.py
   ```

### Configuración usando Docker

Si preferis usar Docker para levantar el entorno, ejecuta el siguiente comando para armar la imagen:

```bash
docker build . -t meli-challenge
```

Recorda pasar las variables de entorno necesarias al contenedor.
En caso contrario se puede pasar un archivo env usando el flag --env-file 


## Base de datos
La base de datos para la aplicacion se despliega automaticamente al iniciar la aplicacion.
Dentro de la carpeta SQL se encuentran valores por defecto para las reglas, que deberan ser cargados y ademas una base de datos para probar las reglas.

## Variables de entorno

### Base de datos para la aplicación
Se eligió MySQL por simplicidad, pero al usar SQLAlchemy, se puede cambiar a cualquier otro motor de base de datos soportado por la librería.

```
* MYSQL_USER: Usuario de la base de datos
* MYSQL_PASSWORD: Contraseña de la base de datos
* MYSQL_HOST: Host de la base de datos
* MYSQL_PORT: Puerto de la base de datos
* MYSQL_DB: Nombre de la base de datos
```

## Secretos para la aplicación
```
* SECRET_KEY: Clave utilizada para el cifrado AES CBC. Tiene que ser de 16, 24 o 32 caracteres
```

## Estructura del Proyecto

```plaintext
├── .dockerignore       # Especifica archivos y directorios ignorados en las construcciones de Docker
├── .env                # Archivo para las variables de entorno
├── .gitignore          # Especifica los archivos que Git debe ignorar
├── Dockerfile          # Instrucciones para construir la imagen Docker de la aplicación
├── README.md           # Documentación del proyecto
├── requirements.txt    # Dependencias necesarias para ejecutar la aplicación
├── src/                # Código fuente de la aplicación
│   ├── core/           # Módulos centrales de la lógica de la aplicación
│   │   ├── __init__.py # Hace que Python trate al directorio como un paquete
│   │   ├── analyzer.py # Lógica para analizar y clasificar datos
│   │   ├── encryption.py # Funciones para manejar cifrado
│   ├── database/       # Interacción con la base de datos
│   │   ├── __init__.py 
│   │   ├── db.py       # Configuración de conexión a la base de datos
│   ├── models/         # Modelos de la base de datos
│   │   ├── __init__.py 
│   │   ├── database.py 
│   │   ├── rule.py     # Modelo de reglas de clasificación
│   │   ├── scan.py     # Modelo de resultados de escaneo
│   ├── routes/         # Rutas de la API
│   │   ├── __init__.py 
│   │   ├── database.py 
│   │   ├── rule.py     # Rutas para gestionar reglas
│   │   ├── scan.py     # Rutas para realizar escaneos
│   ├── __init__.py 
│   ├── main.py         # Punto de entrada principal de la aplicación
└── challenge.md        # Documentación del challenge para Mercado Libre
```


## Uso de la Aplicación
### Clasificación de Datos en la Base de Datos

Para realizar la clasificación de datos sensibles en las bases de datos registradas, debes utilizar el endpoint específico para escanear una base de datos. Podes hacer esto mediante el siguiente comando usando cURL o cualquier cliente HTTP que prefieras:

```bash
curl -X POST http://localhost:8000/api/v1/database/scan/{id} -H 'Content-Type: application/json' -d '{"id": "uuid-del-database"}'
```

Este comando enviará una solicitud para iniciar un escaneo en la base de datos especificada por el UUID proporcionado. Asegúrate de reemplazar `{id}` con el identificador UUID de la base de datos que deseas escanear. Este UUID debe ser uno de los que están registrados en tu sistema y puedes obtenerlos listando las conexiones:

```bash
curl http://localhost:8000/api/v1/database
```

### Documentación API - Swagger

La documentación completa de la API está disponible a través de Swagger UI, para explorar todos los endpoints disponibles y sus especificaciones. Podes acceder a esta interfaz navegando a:

```
http://localhost:8000/docs
```

En la documentación de Swagger, encontrarás detalles sobre cómo realizar peticiones a cada endpoint, los parámetros requeridos, y las respuestas esperadas. Esto incluye operaciones para:

- **Obtener conexiones**: Listar todas las bases de datos registradas.
- **Registrar una nueva conexión**: Añadir una nueva base de datos al sistema.
- **Actualizar una regla de clasificación**: Modificar una regla existente.
- **Eliminar una regla**: Remover una regla de clasificación del sistema.


### Ejemplo de Clasificación

La aplicación buscará patrones predefinidos como correos electrónicos, números de tarjetas de crédito, direcciones IP, entre otros, y los clasificará. A continuación, un ejemplo de cómo se verían los resultados:

```json
{
  "table": "users",
  "columns": [
    {
      "column_name": "ip_address",
      "column_type": "VARCHAR(45)",
      "classification_by_name": "IP_ADDRESS",
      "classification_by_data": "IP_ADDRESS_VALUE"
    },
    {
      "column_name": "username",
      "column_type": "VARCHAR(50)",
      "classification_by_name": "NAME",
      "classification_by_data": "N/A"
    },
    {
      "column_name": "street_address",
      "column_type": "VARCHAR(100)",
      "classification_by_name": "ADDRESS",
      "classification_by_data": "N/A"
    },
    {
      "column_name": "cuil_cuit_dni",
      "column_type": "VARCHAR(20)",
      "classification_by_name": "N/A",
      "classification_by_data": "CUIL/CUIT/DNI"
    }
  ],
  "created": "2024-09-20T10:57:37"
}
```

## Mejoras Futuras

- Implementar una interfaz gráfica para facilitar la interacción con la aplicación.
- Integración con servicios de monitoreo de seguridad para alertas en tiempo real.
- Optimización del rendimiento en bases de datos de gran tamaño.
