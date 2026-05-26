import os
import sys

# Add the repo root (parent of api/) to sys.path so portfolio.py is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from portfolio import app as flask_app

app = flask_app