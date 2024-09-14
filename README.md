# Challenge para Mercado Libre - Data Sec

## Variables de entorno

### Base de datos para la aplicación
Se eligio MySQL por simplicidad, pero al usar sqlalchemy, se puede cambiar a cualquier otro motor de base de datos soportado por la libreria.
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