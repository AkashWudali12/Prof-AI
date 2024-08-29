FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD exec gunicorn --bind :$PORT --workers 2 --threads 8 --timeout 0 app:app