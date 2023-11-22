FROM python:3.11-bookworm

ENV PYTHONBUFFERED=1

WORKDIR /docker_storefront

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD gunicorn storefront.wsgi:application --bind 0.0.0.0:8001

EXPOSE 8001




















