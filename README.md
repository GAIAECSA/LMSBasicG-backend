# LMS-BackEND

levantar contenedor

Entrar a contenedor para migrar


PYTHONPATH=/app python -m app.scripts.create_tables
docker exec -it fastapi_app_mdt_lms bash


docker stop fastapi_app_mdt_lms
docker rm fastapi_app_mdt_lms
docker build -t mdt_lms-api .
docker run -d \
  --name fastapi_app_mdt_lms \
  --restart unless-stopped \
  -p 9002:9002 \
  --env-file .env \
  mdt_lms-api
  docker logs -f fastapi_app_mdt_lms

  # creacion de subdirectorios

  mkdir -p /root/mdt_data/demo/uploads
  cp -a uploads/. /root/mdt_data/demo/uploads/    # solo para copiar
  ls -lah /root/mdt_data/demo/uploads