FROM python:3.7

WORKDIR .

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5003

COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]