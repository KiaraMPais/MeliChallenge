Challenge
* API REST
* Python
* Función: Que permita clasificar cualquier base de datos (MySQL)

Datos:
* La clasificación puede realizarse basándonoslos en:
    * Escaneando muestra información contenida en tablas con un DLP. (No pareciera ser el caso)
    * Nombre de tablas y columnas
        * Buscando en base al nombre de las columnas (FIRST_NAME, LAST_NAME, CREDIT_CARD_NUMBER)

Caso - Clasificación de base de datos
Contexto
En la actualidad se manejan una gran cantidad de datos personales, los cuales tienen que ser identificados y clasificados para poder aplicar los controles y restricciones correspondientes, de manera que se pueda minimizar el riesgo de una fuga de información al mínimo posible.
Objetivo
1.- Desarrollar una API REST en Golang / Python que permita clasificar como se indica más abajo, en principio, cualquier base de datos MySQL.
La clasificación de una base de datos relacional, puede realizarse basándose en el nombre de las tablas y/o columnas, y/o escaneando una muestra de la información contenida en las tablas con un DLP.
En este caso podrá hacerse sólo en base al nombre de las columnas de cada tabla, acotando la búsqueda a una lista de tipos de información a identificar (por ejemplo: FIRST_NAME, LAST_NAME, IP_ADDRESS, CREDIT_CARD_NUMBER, etc.) utilizando expresiones regulares, documentando los mismos y considerando sólo el idioma inglés.
Deberá ser posible agregar nuevos tipos de información a contemplar en los escaneos en cualquier momento.
El resultado esperado será identificar dentro de una base de datos, toda la estructura de sus esquemas y tablas, y el tipo de información almacenada a nivel de columna, por ejemplo para una tabla “USERS”:

TABLE: USERS
COLUMN
	INFORMATION_TYPE

id	N/A
username	USERNAME
useremail	EMAIL_ADDRESS
credit_card_number	CREDIT_CARD_NUMBER
created_timestamp	N/A
Se deberá contar con una base de datos MongoDB ó MySQL (según lo que se considere mejor para persistir la información del resultado de los escaneos) donde almacenar al menos: configuraciones, historial de escaneos, y la estructura y clasificación actualizada a partir del último escaneo de cada base de datos.
Para ello, la API deberá contar mínimamente con los siguientes endpoints para cubrir la funcionalidad solicitada:
POST /api/v1/database Persistir los datos de conexión de una base de datos MySQL a escanear (host, puerto, usuario y contraseña) almacenados de forma segura.
Body:
Nombre	Tipo	Descripción
host	string	Indica la ip o DNS al cual conectarse
port	integer	Indica el puerto por el cual tiene que conectarse
username	string	Indica el nombre de usuario de la base de datos
password	string	Indica la contraseña del usuario de la base de datos
Respuesta:
● En caso de éxito:
* 		○  Status code: 201. 
* 		○  Body: el id del objeto creado en la base de datos. 

● En caso de error:
* 		○  Status code: el que corresponda al tipo de error. 
* 		○  Body: un mensaje descriptivo del error.  POST /api/v1/database/scan/:id Ejecutar la clasificación de una base de datos dado un id asociado a la misma.  Parámetros:  Respuesta: 
● En caso de éxito:
○ Status code: 201. ● En caso de error:
* 		○  Status code: el que corresponda al tipo de error. 
* 		○  Body: un mensaje descriptivo del error.  GET /api/v1/database/scan/:id Obtener la estructura y clasificación de una base de datos dado un id asociado a la misma.  Parámetros:  Respuesta: 
● En caso de éxito:
* 		○  Status code: 200. 
* 		○  Body: JSON con la estructura de la base de datos, conteniendo sus esquemas, tablas y columnas. Por cada columna se deberá especificar el tipo de dato encontrado. 
Nombre	Tipo	Descripción
id	integer	Id de la base de datos a escanear
Nombre	Tipo	Descripción
id	integer	Id de una base de datos ya escaneada para obtener su estructura y clasificación

● En caso de error:
* 		○  Status code: el que corresponda al tipo de error. 
* 		○  Body: un mensaje descriptivo del error.  Queda a criterio del colaborador agregar por lo menos 1 funcionalidad que ayude al objetivo de identificación de datos en MySQL, teniendo en cuenta que la identificación actual sólo se basa en el nombre de las columnas.  2. Proponer un listado de controles y restricciones que podría un equipo de datasecurity aplicar segun la clasificación de una BD que permita minimizar el riesgo de una fuga de información al mínimo posible.  Entregables  Pto 1 
* 		●  Repositorio en Github del código fuente o un .zip con el código fuente. 
* 		●  Dockerfile correspondiente para ejecutar la aplicación. 
* 		●  Script SQL para crear la base de datos de la aplicación. 
* 		●  Script SQL para crear una base de datos de ejemplo a escanear. 
* 		●  Documentación de la estrategia y solución. 
* 		●  Testing  Pto 2 
* 		●  Listado de controles aplicables para proteger una bd segun su clasificacion  Bonus 
* 		●  Logging 
* 		●  Autenticación en la api 
* 		●  Endpoint para obtener el resumen del resultado de un escaneo de una base de datos  renderizado en HTML, con métricas de interés en relación a los tipos de datos encontrados.  Consideraciones generales 

* 		●  No se pueden utilizar herramientas open-source o comerciales que ya resuelvan este problema. 
* 		●  Se podrán crear todas las funciones complementarias que se consideren necesarias para un correcto funcionamiento de la aplicación. 
* 		●  Se recomienda modularizar y aplicar buenas prácticas de programación para un mejor entendimiento del código. 
* 		●  Toda decisión asumida en cuanto a los requerimientos o desarrollo, deberá ser debidamente documentada. 

