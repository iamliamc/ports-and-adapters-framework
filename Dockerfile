FROM python:3.11

WORKDIR /usr/src/app

EXPOSE 80 9090 5000

COPY requirements.txt /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

CMD ["uvicorn", "sensor_app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
