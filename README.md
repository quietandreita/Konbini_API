# Documentación del Backend

## 1. Introducción
Este proyecto implementa una API REST con CRUD completo para 5 tablas de una base de datos.  
El backend está diseñado para ser consumido por un frontend en Angular.

---

## 2. Requisitos previos
Para ejecutar correctamente el backend es necesario contar con:
- Python 3.10 o superior
- Flask
- Flask-SQLAlchemy
- Flask-CORS
- Flask-JWT-Extended (para autenticación con tokens JWT)
- Werkzeug (para manejo de contraseñas con hash)
- Base de datos MySQL
- Postman (opcional, para pruebas de los endpoints)

### Instalación de dependencias
Ejecutar en la terminal dentro del entorno virtual:

pip install flask flask-sqlalchemy flask-cors flask-jwt-extended werkzeug

---

## 3. Estructura del proyecto
/backend
app.py              # Punto de entrada de la API
models.py           # Definición de las tablas
routes/             # Endpoints CRUD por entidad
config.py           # Configuración de la base de datos

---

## 4. Base de datos
La base de datos contiene 5 tablas:
- Usuario
- Producto
- Categoria
- Pedido
- Detalle Pedido

---

## 5. Endpoints principales
### Usuario
- GET /usuarios
- POST /usuarios
- GET /usuarios/<id>
- PUT /usuarios/<id>
- DELETE /usuarios/<id>

### Producto
- GET /productos
- POST /productos
- GET /productos/<id>
- PUT /productos/<id>
- DELETE /productos/<id>

---

## 6. Despliegue del Backend
1. Clonar el repositorio o copiar la carpeta del proyecto.
2. Configurar la conexión a la base de datos en config.py:
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://usuario:password@localhost/konbini'
3. Inicializar la base de datos:
   flask db init
   flask db migrate
   flask db upgrade
4. Ejecutar el servidor:
   python app.py

El backend quedará disponible en:
http://localhost:5000
