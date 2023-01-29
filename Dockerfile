FROM python:3.8.16-bullseye
ENV PYTHONUNBUFFERED=1
WORKDIR /contact_app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .