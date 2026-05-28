# LMS-BackEND

levantar contenedor

Entrar a contenedor para migrar


PYTHONPATH=/app python -m app.scripts.create_tables


docker run -d \
  --name fastapi_app_mdt_lms \
  --restart unless-stopped \
  -p 9002:9002 \
  mdt_lms-api