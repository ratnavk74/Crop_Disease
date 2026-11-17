FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    TF_CPP_MIN_LOG_LEVEL=2

WORKDIR /app

# OpenCV/TensorFlow runtime libraries.
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgl1 libglib2.0-0 libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt gunicorn

COPY . .

RUN mkdir -p static/uploads

EXPOSE 8000

CMD ["sh", "-c", "gunicorn wsgi:app --bind 0.0.0.0:${PORT:-8000} --workers 1 --threads 4 --timeout 180 --access-logfile -"]
