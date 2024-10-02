FROM python:3.12.6-slim-bookworm

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential libmariadb-dev pkg-config \
    && python3 -m pip install --no-cache-dir --upgrade pip

COPY . /home/program/app
WORKDIR /home/program/app

RUN chmod +r requirements.txt

RUN python3 -m pip install --no-cache-dir --requirement requirements.txt

EXPOSE 5000

CMD [ "python3", "server.py" ]