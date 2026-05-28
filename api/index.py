import sys
import os

# Add parent directory to path so we can import portfolio
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from portfolio import app

# Export app for Vercel
__all__ = ['app']
