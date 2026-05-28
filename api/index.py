import sys
import os
from werkzeug.wsgi import wrap_file

# Add parent directory to path so we can import portfolio
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from portfolio import app as flask_app

# Export app for Vercel serverless
app = flask_app

# Ensure Flask can find static files
@app.after_request
def set_cache_headers(response):
    """Set cache headers for static files"""
    if response.path and (response.path.startswith('/public/') or 
                         response.path.endswith('.css') or 
                         response.path.endswith('.js') or
                         response.path.endswith('.png') or
                         response.path.endswith('.jpg') or
                         response.path.endswith('.svg')):
        response.cache_control.max_age = 3600
        response.cache_control.public = True
    return response
