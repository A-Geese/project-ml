#!/bin/bash

# Create a virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip setuptools wheel
pip install uv
uv pip install -r pyproject.toml

echo "Environment setup complete. Virtual environment is activated!"
