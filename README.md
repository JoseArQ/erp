# 🚀 Django REST API — Docker Setup

Este proyecto utiliza **Django REST Framework** junto con **Docker Compose** para simplificar el despliegue y la ejecución en entornos locales o de desarrollo.

---

## 🧩 Requisitos previos

Asegúrate de tener instalado:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

Verifica la instalación ejecutando:

```bash
docker -v
docker compose version
```

Asegurate de crear el archivo .env en la raíz del proyecto y agregar las variables de entorno requeridas, para ello te puedes basar en el archivo .env-example. 
Ten en cuenta que las variables DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD se usan para crear un super usuario al ejecutarse, esto es importante porque con estos datos se ingresara al admin de Django para configurar los primeros registros para Company y Entity. 

## Ejecutar el proyecto

Para ejecutar el proyecto con docker usar el siguiente comando 

```bash
docker compose up -d
```

Para detener la ejecuación puedes usar los siguientes comandos

```bash
docker compose stop
```

```bash
docker compose down
```

## Ejemplos 

Registrar un usuario 

```bash
curl --location 'http://localhost:8000/users/register/' \
--header 'Content-Type: application/json' \
--data-raw '{
  "username": "jdoeCompany4",
  "email": "jdoe@example.com",
  "password": "securePass123",
  "first_name": "John",
  "last_name": "Doe",
  "role": "employee",
  "company_id": 1
}
'
```

Iniciar sesión 

```bash
curl --location 'http://localhost:8000/users/login/' \
--header 'Content-Type: application/json' \
--data '{
  "username": "jdoeCompany4",
  "password": "securePass123"
}'
```
Cargar documento: Tener en cuenta usar el access token dado en el login
```bash
curl --location 'http://localhost:8000/api/documents/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxNDA3MDQzLCJpYXQiOjE3NjE0MDM0NDMsImp0aSI6ImZiMzM5NzU5MDAyZTQ4OTk5NDBmZmI4MjZkMGRmZWVjIiwidXNlcl9pZCI6IjYifQ.3qW0SHLnAfGZSkNVTtptom8mDA9ZHHK4_P7y2egobBc' \
--form 'file=@"postman-cloud:///1f0b11a4-07df-4cf0-afd4-9182b3093f94"' \
--form 'entity.id="f9d6f75a-4777-40f8-a3f2-9a559c974aff"' \
--form 'company.id ="1"' \
--form 'doc_type ="invoice"'
```

Descargar document: Tener en cuenta usar el access token dado en el login
```bash
curl --location --request GET 'http://localhost:8000/api/documents/4fd61585-5b1b-4a20-9478-bc0c5217ced7' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxNDA3MDQzLCJpYXQiOjE3NjE0MDM0NDMsImp0aSI6ImZiMzM5NzU5MDAyZTQ4OTk5NDBmZmI4MjZkMGRmZWVjIiwidXNlcl9pZCI6IjYifQ.3qW0SHLnAfGZSkNVTtptom8mDA9ZHHK4_P7y2egobBc' \
--form 'file=@"postman-cloud:///1f0b11a4-07df-4cf0-afd4-9182b3093f94"' \
--form 'entity.id="f9d6f75a-4777-40f8-a3f2-9a559c974aff"' \
--form 'company.id ="1"' \
--form 'doc_type ="invoice"'
```

Aprobar documento: Tener en cuenta usar el access token dado en el login para un usuario administrador
```bash
curl --location 'http://localhost:8000/api/documents/4fd61585-5b1b-4a20-9478-bc0c5217ced7/approve/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxNDA3MDQzLCJpYXQiOjE3NjE0MDM0NDMsImp0aSI6ImZiMzM5NzU5MDAyZTQ4OTk5NDBmZmI4MjZkMGRmZWVjIiwidXNlcl9pZCI6IjYifQ.3qW0SHLnAfGZSkNVTtptom8mDA9ZHHK4_P7y2egobBc' \
--header 'Content-Type: application/json' \
--data '{
    "comment": "documento revisado exitosamente"
}'
```

Rechazar documento: Tener en cuenta usar el access token dado en el login para un usuario administrador

```bash
curl --location 'http://localhost:8000/api/documents/d6a0c6a3-0897-4819-bb2f-7cad2253f8a6/reject/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxMzUxMzIxLCJpYXQiOjE3NjEzNDc3MjEsImp0aSI6IjQwM2IzMzIyZTZjZDQ5MTk4Y2Q0ZWUxNGRhMzA0NGYxIiwidXNlcl9pZCI6IjIifQ.dYsaLq7B0rID6KmcujPv-TlEAMHVwegjTaXP3COnCkQ' \
--header 'Content-Type: application/json' \
--data '{
    "comment": "documento revisado invalido"
}'
```