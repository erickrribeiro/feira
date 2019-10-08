import os
import datetime

from flask import Flask, jsonify
from flask_caching import Cache
from flask_limiter import Limiter, HEADERS
from flask_limiter.util import get_remote_address

from weather import Weather

TOKEN = os.environ['TOKEN_OPEN_WEATHER_MAP']
weather = Weather(token=TOKEN)

app = Flask(__name__)
# app.config['DEBUG'] = True
app.config['RATELIMIT_STORAGE_URL'] = 'redis://localhost:6379'
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379'

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["50 per minute"],
)

limiter._header_mapping[HEADERS.LIMIT] = 'X-My-Limit'
cache = Cache(app)


@app.route("/weather/<id>", methods=['GET'])
@cache.cached(timeout=60*5)
@limiter.limit("50 per minute")
def weather_info(id):
    return jsonify({
        'message': weather.fetch(city_id=id, date=datetime.datetime.now())
    })


if __name__ == "__main__":
    app.run()
