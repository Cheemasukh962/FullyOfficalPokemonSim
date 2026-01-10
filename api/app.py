"""Platform entrypoint - imports Flask app from source."""
import sys
import os

# Add project root to path so we can import modules like `source.api.server`
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

# Import the Flask app from the server module
from source.api.server import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
