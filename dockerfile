FROM python:3.11

RUN apt-get update

WORKDIR /usr/src/app
COPY requirements.txt .

RUN pip3 install -r requirements.txt

EXPOSE 8050

COPY . .

CMD [ "python","app.py" ]