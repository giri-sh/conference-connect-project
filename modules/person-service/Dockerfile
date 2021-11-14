FROM python:3.7-alpine

WORKDIR .

RUN pip3 install --upgrade pip
RUN apk add --no-cache g++ gcc musl-dev linux-headers geos libc-dev postgresql-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5001

COPY . .
CMD ["python", "./app/main.py"]