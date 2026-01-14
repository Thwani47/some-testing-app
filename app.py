from flask import Flask, jsonify
import os

app = Flask(__name__)

import redis
import os

# Redis connection
redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = int(os.getenv('REDIS_PORT', 6379))
r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

@app.route('/count')
def count():
    """Increment and return visit count using Redis"""
    count = r.incr('visit_count')
    return jsonify({
        'visit_count': count,
        'app': 'some-testing-app',
        'redis_connected': True
    })

@app.route('/health/redis')
def redis_health():
    """Check Redis connection"""
    try:
        r.ping()
        return jsonify({'status': 'healthy', 'redis': 'connected'})
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500


@app.route('/')
def hello():
    return jsonify({
        'message': 'Hello from some-testing-app!',
        'app': 'some-testing-app',
        'version': '1.0.0',
        'redis_enabled': True
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
