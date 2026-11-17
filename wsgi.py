"""WSGI entry point for gunicorn / production servers.

Usage:
    gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 180
"""

import os

from app import app

# Ensure runtime folders exist when the container starts.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(BASE_DIR, "static", "uploads"), exist_ok=True)

application = app
