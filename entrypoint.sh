#!/bin/bash
#
# Description:
# Production !!!

set -e

gunicorn \
  --workers 8 \
  --bind 0.0.0.0:8050 \
  --log-level debug \
  --timeout 5000 \
  app:app