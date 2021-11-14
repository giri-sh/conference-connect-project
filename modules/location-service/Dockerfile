FROM python:3.7

WORKDIR .

RUN apk add --no-cache g++ gcc musl-dev linux-headers geos libc-dev postgresql-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5002

COPY . .
CMD ["python", "./app/main.py"]