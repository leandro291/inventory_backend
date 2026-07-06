# Boot-Python API

API RESTful para gestión de inventario y productos, desarrollada con Flask.

## Stack Tecnológico

- **Framework:** Flask 3.1 + Flask-RESTful
- **ORM:** SQLAlchemy 2.0 + Flask-Migrate (Alembic)
- **Base de datos:** PostgreSQL (Neon)
- **Autenticación:** JWT (Flask-JWT-Extended)
- **Validación:** Pydantic 2
- **Documentación:** Flasgger (Swagger UI)
- **Imágenes:** Cloudinary
- **Hash:** bcrypt

## Instalación

```bash
# Clonar repositorio
git clone <repo-url>
cd backend-repo

# Crear entorno virtual
python -m venv venv

# Activar (Windows)
.\venv\Scripts\activate

# Activar (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Configuración

Crear archivo `.env` en la raíz:

```env
DB_URI="postgresql://usuario:password@host:5432/db?sslmode=require"
SECRET_KEY="tu_secret_key"
JWT_SECRET_KEY="tu_jwt_secret_key"
FERNET_SECRET_KEY="tu_fernet_key"

CLOUDINARY_CLOUD_NAME="tu_cloud"
CLOUDINARY_API_KEY="tu_api_key"
CLOUDINARY_API_SECRET="tu_api_secret"
```

> Puedes generar las keys con: `python key_generator.py`

## Base de Datos

```bash
# Inicializar migraciones
flask db init

# Crear migración
flask db migrate -m "descripcion"

# Aplicar migraciones
flask db upgrade
```

## Ejecutar

```bash
python run.py
```

La API corre en `http://localhost:5000`

## Documentación Swagger

Disponible en `http://localhost:5000/apidocs/`

## Endpoints

Todas las rutas usan el prefijo `/api/v1`.

### Auth

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/auth/login` | Iniciar sesión |
| POST | `/auth/register` | Registrar usuario |

### Categorías

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/category` | Listar categorías |
| POST | `/category` | Crear categoría |
| GET | `/category/{id}` | Obtener categoría |
| PUT | `/category/{id}` | Actualizar categoría |
| DELETE | `/category/{id}` | Eliminar categoría |

### Productos

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/product` | Listar productos |
| POST | `/product` | Crear producto (multipart) |
| GET | `/product/{id}` | Obtener producto |
| PUT | `/product/{id}` | Actualizar producto (multipart) |
| DELETE | `/product/{id}` | Eliminar producto |

### Empresas

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/company` | Listar empresas |
| POST | `/company` | Crear empresa |
| GET | `/company/{id}` | Obtener empresa |
| PUT | `/company/{id}` | Actualizar empresa |
| DELETE | `/company/{id}` | Eliminar empresa |

### Proveedores

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/supplier` | Listar proveedores |
| POST | `/supplier` | Crear proveedor |
| GET | `/supplier/{id}` | Obtener proveedor |
| PUT | `/supplier/{id}` | Actualizar proveedor |
| DELETE | `/supplier/{id}` | Eliminar proveedor |

### Almacenes

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/repository` | Listar almacenes |
| POST | `/repository` | Crear almacén |
| GET | `/repository/{id}` | Obtener almacén |
| PUT | `/repository/{id}` | Actualizar almacén |
| DELETE | `/repository/{id}` | Eliminar almacén |

### Tipos de Movimiento

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/type-movement` | Listar tipos |
| POST | `/type-movement` | Crear tipo |
| GET | `/type-movement/{id}` | Obtener tipo |
| PUT | `/type-movement/{id}` | Actualizar tipo |
| DELETE | `/type-movement/{id}` | Eliminar tipo |

### Roles

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/role` | Listar roles |
| POST | `/role` | Crear rol |
| GET | `/role/{id}` | Obtener rol |
| PUT | `/role/{id}` | Actualizar rol |
| DELETE | `/role/{id}` | Eliminar rol |

### Inventario

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/inventory` | Listar inventario |
| POST | `/inventory` | Crear o acumular stock |
| GET | `/inventory/{id}` | Obtener inventario |
| PUT | `/inventory/{id}` | Actualizar inventario |
| DELETE | `/inventory/{id}` | Eliminar inventario |

### Movimientos

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/movement` | Listar movimientos |
| POST | `/movement` | Crear movimiento (entrada/salida) |
| GET | `/movement/{id}` | Obtener movimiento |
| DELETE | `/movement/{id}` | Eliminar movimiento |

## Estructura del Proyecto

```
backend-repo/
├── app/
│   ├── __init__.py          # Factory de la app, config Swagger
│   ├── router.py            # Registro de rutas
│   ├── models/              # Modelos SQLAlchemy (11 entidades)
│   ├── schemas/             # Schemas Pydantic de validación
│   ├── resources/           # Recursos Flask-RESTful (endpoints)
│   ├── services/            # Lógica de negocio
│   └── utils/
│       └── helpers.py       # Password, Crypto, Cloudinary
├── migrations/              # Migraciones Alembic
├── config.py                # Configuración de la app
├── db.py                    # Instancia de SQLAlchemy
├── key_generator.py         # Generador de keys
├── requirements.txt
└── run.py                   # Punto de entrada
```
