#!/bin/sh

export PATH=$HOME/.local/bin:$PATH


# Start Uvicorn with live reload
exec uvicorn --reload --port $PORT example_project.main:app