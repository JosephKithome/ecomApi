FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt  requirements.txt

RUN pip3 install -r requirements.txt
RUN pip install --upgrade pip
RUN pip install psycopg2-binary

# Copy project
COPY . /app/

CMD ["python3","manage.py","runserver","0.0.0.0:8000"]