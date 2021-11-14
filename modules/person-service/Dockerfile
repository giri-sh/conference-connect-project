FROM python:3.7

WORKDIR .

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5001

COPY . .
CMD ["python", "./app/main.py"]