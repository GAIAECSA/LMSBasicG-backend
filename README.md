# LMS-BackEND

levantar contenedor

Entrar a contenedor para migrar


PYTHONPATH=/app python -m app.scripts.create_tables
docker exec -it fastapi_app_mdt_lms bash


# Pasos
mkdir -p /root/mdt_data/demo/uploads

docker stop fastapi_app_mdt_lms
docker rm fastapi_app_mdt_lms
docker build -t mdt_lms-api .
docker run -d \
  --name fastapi_app_mdt_lms \
  --restart unless-stopped \
  -p 9002:9002 \
  --env-file .env \
  -v /root/mdt_data/demo/uploads:/app/uploads \
  -v /opt/lmsbasicg/secrets:/opt/lmsbasicg/secrets:ro \
  mdt_lms-api
docker inspect fastapi_app_mdt_lms
docker logs -f fastapi_app_mdt_lms
# Fin pasos

mkdir -p /root/mdt_data/demo/uploads

docker run -d \
  --name fastapi_app_mdt_lms \
  --restart unless-stopped \
  -p 9002:9002 \
  --env-file .env \
  -v /root/mdt_data/demo/uploads:/app/uploads \
  mdt_lms-api

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


  docker volume create athena_uploads

  # creacion de subdirectorios

  mkdir -p /root/mdt_data/demo/uploads
  cp -a uploads/. /root/mdt_data/demo/uploads/    # solo para copiar
  ls -lah /root/mdt_data/demo/uploads


  # no se que hace

  root@ubuntu:~# root@ubuntu:~# mkdir -p /opt/lmsbasicg/secrets
root@ubuntu:~# openssl genpkey \
>   -algorithm RSA \
>   -out /opt/lmsbasicg/secrets/gaia-lti-private.pem \
>   -pkeyopt rsa_keygen_bits:2048
...+....+......+........+.+...+..+.........+.......+.....+.........................+.....+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*.+.....+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*..........+...+..........+.....+...............................+......+.....+................+..+...+...+.......+..+.......+.....+.+.................+...+...+....+......+............+.....+....+.....+...+.+.........+...+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
.........+.+..+..........+.........+...+...+...+.....................+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*....+.......+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*...................+....+..+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
root@ubuntu:~# chmod 600 /opt/lmsbasicg/secrets/gaia-lti-private.pem
root@ubuntu:~# openssl rand -hex 32