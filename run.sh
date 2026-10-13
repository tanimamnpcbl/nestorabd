#!/usr/bin/env bash
set -e
gunicorn nestora.wsgi:application --bind "0.0.0.0:${PORT:-8000}" --log-file -
