from flask import Flask
from dotenv import load_dotenv
import os
from src.app import register_routes

load_dotenv()
app = Flask(__name__)

register_routes(app)

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
