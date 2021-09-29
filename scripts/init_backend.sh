#!/bin/bash

cd backend
export PIPENV_VENV_IN_PROJECT=1
pipenv install --deploy
.venv/bin/python -m main init_db