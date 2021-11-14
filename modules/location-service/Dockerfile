FROM python:3.7

WORKDIR .

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5002

COPY . .
CMD ["python", "./app/main.py"]