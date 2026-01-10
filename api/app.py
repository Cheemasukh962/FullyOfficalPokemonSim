"""Vercel entrypoint - imports Flask app from source."""
import sys
import os

# Add source to path so we can import server
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from source.api.server import app

# Export app for Vercel
if __name__ == "__main__":
    app.run()
