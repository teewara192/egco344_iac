import logging
from flask import Flask, request

app = Flask(__name__)

# Configure the logger to show info-level messages
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
 # Log the event to the console (STDOUT)
 logger.info(f"--- VISIT DETECTED | Source IP: {request.remote_addr} ---")
 return "<h1>Step 2: Success!</h1><p>I am now logging your visits to the console.</p>"
if __name__ == '__main__':
 app.run(host='0.0.0.0', port=8700)