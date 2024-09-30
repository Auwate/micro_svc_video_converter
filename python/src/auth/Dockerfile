FROM python:3.12.6-slim-bookworm

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential default-libmysqlclient-dev

COPY . /home/program/app
WORKDIR /home/program/app

RUN chmod +r requirements.txt && chmod +x build-script.sh

EXPOSE 5000

CMD [ "./build-script.sh" ]