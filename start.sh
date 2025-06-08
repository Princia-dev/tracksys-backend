#!/usr/bin/env bash

# Démarre uvicorn avec le port fourni par Render
exec uvicorn serveur.backend:app --host 0.0.0.0 --port ${PORT:-8000} --timeout-keep-alive 300