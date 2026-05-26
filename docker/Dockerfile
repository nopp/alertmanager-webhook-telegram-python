FROM python:3.11-slim

LABEL maintainer="Carlos Augusto Malucelli <camalucelli@gmail.com>"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY wsgi.py .

EXPOSE 9119

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:9119", "wsgi:app"]
