FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV PYTHONPATH=src

CMD ["gunicorn", "--bind", "0.0.0.0:1111", "src.main:app"]
