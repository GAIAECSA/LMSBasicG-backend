# LMS-BackEND

levantar contenedor

Entrar a contenedor para migrar


PYTHONPATH=/app python -m app.scripts.create_tables
docker exec -it fastapi_app_mdt_lms bash
docker restart fastapi_app_mdt_lms
docker logs -f fastapi_app_mdt_lms
docker build -t fastapi_app_mdt_lms .

docker stop fastapi_app_mdt_lms
docker rm fastapi_app_mdt_lms

docker run -d \
  --name fastapi_app_mdt_lms \
  --restart unless-stopped \
  -p 9002:9002 \
  mdt_lms-api