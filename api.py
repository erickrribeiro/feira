import os
import datetime
import unicodedata

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

data = {
    'Acre': 3665474,
    'Rio Branco': 3662574,
    'Alagoas': 3408096,
    'Maceió': 6320645,
    'Amapá': 3407762,
    'Macapá': 3396016,
    'Amazonas': 3665361,
    'Manaus': 3663517,
    'Bahia': 3471168,
    'Salvador': 6321026,
    'Ceará': 3402362,
    'Fortaleza': 6320062,
    'Distrito Federal': 3463504,
    'Brasília': 3410315,
    'Espírito Santo': 3463930,
    'Vitória': 3444924,
    'Goiás': 3462372,
    'Goiânia': 6323974,
    'Maranhão': 3395443,
    'São Luís': 3388368,
    'Mato Grosso': 3457419,
    'Cuiabá': 6323820,
    'Mato Grosso do Sul': 3457415,
    'Campo Grande': 3467747,
    'Minas Gerais': 3457153,
    'Belo Horizonte': 3470127,
    'Pará': 3393129,
    'Belém': 3373305,
    'Paraíba': 3393098,
    'João Pessoa': 3397277,
    'Paraná': 3455077,
    'Curitiba': 6322752,
    'Pernambuco': 3392268,
    'Recife': 3390760,
    'Piauí': 3392213,
    'Teresina': 3386496,
    'Rio de Janeiro': 3451189,
    'Rio Grande do Norte': 3390290,
    'Natal': 3394023,
    'Rio Grande do Sul': 3451133,
    'Porto Alegre': 3452925,
    'Rondônia': 3924825,
    'Porto Velho': 3662762,
    'Roraima': 3662560,
    'Boa Vista': 3664980,
    'Santa Catarina': 3450387,
    'Florianópolis': 6323121,
    'São Paulo': 3448433,
    'Sergipe': 3447799,
    'Aracaju': 3471872,
    'Tocantins': 3474575,
    'Palmas': 3455459
}
name2id = dict()
for key in data.keys():
    value = data[key]
    key = unicodedata.normalize('NFKD', key).encode('ASCII', 'ignore')
    key = key.lower()
    name2id[key] = value


@app.route("/weather/<name>", methods=['GET'])
@cache.cached(timeout=60*60*24)
@limiter.limit("50 per minute")
def weather_info(name):
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore')
    name = name.lower()
    id_ = name2id[name]

    return jsonify({
        'message': weather.fetch(city_id=id_, date=datetime.datetime.now())
    })


if __name__ == "__main__":
    app.run()
