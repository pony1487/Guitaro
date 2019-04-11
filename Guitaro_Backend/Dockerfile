FROM python:3.6

RUN apt-get -y update
RUN apt-get -y upgrade

RUN pip install --upgrade pip

RUN apt-get install -y libasound-dev portaudio19-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

#VOLUME /audio

EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]