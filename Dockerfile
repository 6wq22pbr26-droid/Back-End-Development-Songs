FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PORT=3000
EXPOSE 3000
USER 1001
CMD ["sh", "-c", "exec gunicorn --bind 0.0.0.0:${PORT:-3000} --workers 1 --threads 4 --access-logfile - app:app"]
