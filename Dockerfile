from python:3.10-slim-buster

# Too much time to debug this plus unit tests so just placeholder for now

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["python", "entrypoint.py"]