import os
from flask import Flask
from redis import Redis

app = Flask(__name__)

# Connect to Redis
# If running locally, host is usually 'localhost'
# If using Docker, host is the name of the service (e.g., 'redis')
# Use 'redis' (the service name in docker-compose) as the default host
redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_client = Redis(host=redis_host, port=6379, decode_responses=True)

@app.route('/')
def index():
 try:
    # The 'incr' command adds 1 to the key 'hits'.
    # If 'hits' doesn't exist, Redis creates it and sets it to 1.
    hits = redis_client.incr('hits')
 except Exception as e:
    return f"Could not connect to Redis: {e}", 500

 return f"""
 <html>
    <head><title>Redis Visitor Counter</title></head>
    <body style="text-align: center; padding-top: 50px; font-family:sans-serif; background-color: #f4f4f9;">
        <div style="display: inline-block; border: 2px solid #ff4500; padding: 20px; border-radius: 10px; background: white;">
            <h1 style="color: #ff4500;">EGCO344 Counter</h1>
            <p style="font-size: 1.2em;">This page has been viewed</p>
            <p style="font-size: 3em; font-weight: bold; margin: 10px 0;">{hits}</p>
            <p style="font-size: 1.2em;">times.</p>
        </div>
    </body>
 </html>
 """
 
if __name__ == '__main__':
 app.run(host='0.0.0.0', port=5050)