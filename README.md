# Sistema de Gestión de Biblioteca

Una API REST desarrollada con Django para gestionar una biblioteca de libros. Este proyecto implementa operaciones CRUD completas, paginación, filtros por autor y un conjunto completo de pruebas unitarias.

## Características del Sistema

El sistema permite realizar las siguientes operaciones:
- Crear, leer, actualizar y eliminar libros
- Paginar los resultados mostrando 10 libros por página
- Filtrar libros por nombre del autor usando parámetros de consulta
- Validar que el stock no sea negativo
- Verificar que no existan ISBN duplicados
- Buscar libros por título o autor

## Configuración Inicial del Proyecto

### Paso 1: Preparar el Entorno

Primero necesitas tener Python instalado en tu sistema. Luego instala las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

### Paso 2: Configurar la Base de Datos

Navega al directorio del proyecto y crea las migraciones para la base de datos:

```bash
cd biblioteca
python manage.py makemigrations
```

Aplica las migraciones para crear las tablas necesarias:

```bash
python manage.py migrate
```

### Paso 3: Crear un Usuario Administrador (Opcional)

Si quieres acceder al panel de administración de Django, crea un superusuario:

```bash
python manage.py createsuperuser
```

Sigue las instrucciones para establecer el nombre de usuario, email y contraseña.

### Paso 4: Iniciar el Servidor

Ejecuta el servidor de desarrollo:

```bash
python manage.py runserver
```

El servidor estará disponible en http://localhost:8000

## Endpoints de la API

La API proporciona los siguientes endpoints para gestionar los libros:

### Operaciones Básicas

**Listar todos los libros (con paginación)**
```
GET /api/books/
```

**Crear un nuevo libro**
```
POST /api/books/
```

**Obtener un libro específico**
```
GET /api/books/{id}/
```

**Actualizar completamente un libro**
```
PUT /api/books/{id}/
```

**Actualizar parcialmente un libro**
```
PATCH /api/books/{id}/
```

**Eliminar un libro**
```
DELETE /api/books/{id}/
```

### Parámetros de Consulta Disponibles

Puedes usar estos parámetros para filtrar y navegar por los resultados:

- `?author=NombreAutor` - Filtra libros por autor
- `?page=2` - Navega a una página específica
- `?search=palabra` - Busca en títulos y autores

## Ejecutar las Pruebas

### Usando Django TestCase

Para ejecutar todas las pruebas usando el sistema de pruebas de Django:

```bash
python manage.py test
```

### Usando pytest (Recomendado)

Para ejecutar las pruebas con pytest (más detallado y mejor formato):

```bash
pytest
```

### Ejecutar Pruebas Específicas

Si quieres ejecutar una prueba específica:

```bash
pytest biblioteca/tests.py::BookAPITestCase::test_create_valid_book_returns_201
```

## Cobertura de Pruebas

Las pruebas incluyen los siguientes escenarios:

**Creación de Libros**
- Crear un libro válido debe retornar código 201
- Intentar crear un libro con ISBN duplicado debe retornar código 400
- Crear un libro con stock negativo debe retornar código 400

**Consulta de Libros**
- Obtener la lista paginada debe retornar código 200 con estructura de paginación
- Filtrar por autor debe retornar solo los libros de ese autor

**Actualización de Libros**
- Actualizar completamente (PUT) debe persistir todos los cambios
- Actualizar parcialmente (PATCH) debe persistir solo los campos modificados

**Eliminación de Libros**
- Eliminar un libro debe retornar código 204 y el libro no debe existir más

## Ejemplos de Uso de la API

### Crear un Nuevo Libro

```bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Content-Type: application/json" \
  -d '{
    "isbn": "9781234567890",
    "title": "Guía de Django REST Framework",
    "author": "María García",
    "published_date": "2023-01-01",
    "stock": 15
  }'
```

### Filtrar Libros por Autor

```bash
curl "http://localhost:8000/api/books/?author=María García"
```

### Actualizar Solo el Stock de un Libro

```bash
curl -X PATCH http://localhost:8000/api/books/1/ \
  -H "Content-Type: application/json" \
  -d '{"stock": 20}'
```

### Obtener una Página Específica

```bash
curl "http://localhost:8000/api/books/?page=2"
```

## Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

- `models.py` - Define el modelo Book con validaciones
- `serializers.py` - Maneja la serialización y validación de datos
- `views.py` - Contiene las vistas de la API con paginación y filtros  
- `urls.py` - Define las rutas de la API
- `tests.py` - Contiene todas las pruebas unitarias
- `requirements.txt` - Lista las dependencias del proyecto

## Notas Importantes

- La base de datos por defecto es SQLite, adecuada para desarrollo
- El stock de los libros no puede ser negativo
- Los ISBN deben ser únicos en el sistema
- La paginación está configurada para mostrar 10 elementos por página
- El filtro por autor no distingue entre mayúsculas y minúsculas

