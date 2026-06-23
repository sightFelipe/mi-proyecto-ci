# Mi Proyecto CI - Sistema de Gestión de Tareas

Proyecto de software basado en herramientas de integración continua - Énfasis Profesional I

## Integrante

- **[Juan Felipe Peña Márquez]** - Documentación y pruebas

## Arquitectura

El sistema se compone de dos contenedores Docker:

| Contenedor | Tecnología | Puerto |
|------------|------------|--------|
| **backend** | Flask + Python | 5000 |
| **db** | PostgreSQL | 5432 |

## Endpoints de la API

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/health` | Verificación de salud |
| GET | `/api/tasks` | Listar tareas |
| POST | `/api/tasks` | Crear tarea |
| GET | `/api/tasks/<id>` | Obtener tarea |
| PUT | `/api/tasks/<id>` | Actualizar tarea |
| DELETE | `/api/tasks/<id>` | Eliminar tarea |

## Cómo levantar el proyecto

```bash
docker compose up -d"# Travis CI build" 
