#!/bin/sh

echo "Starting production server..."
cd /ubrato/app && poetry run uvicorn main:app --host $SERVER_ADDR --port $SERVER_PORT