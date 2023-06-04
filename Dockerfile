FROM python:3.10-slim-buster

WORKDIR /

RUN pip install --upgrade pip

RUN apt-get update && apt-get install -y ffmpeg build-essential libcairo2-dev pkg-config python3-dev


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .



CMD [ "python3", "client_discord_bot.py"]