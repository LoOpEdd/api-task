from kaufland import HTTPConnection
from flask  import Flask
from flask_restful import Resource, Api, reqparse
import json

kaufland_request = HTTPConnection()

def get_starship_from_name(name):
    url = f'https://swapi.dev/api/starships/?search={name}'
    while url:
        resp = kaufland_request.request('get', url, retries=1)
        starship_data = json.loads(resp.content)
        ship = filter(lambda x: name in x['name'], starship_data['results'])
        for i in ship:
            yield i
        url = starship_data.get('next', None)
    return None

def get_planets_from_pilots(urls):
    for pilot_url in urls:
        resp = kaufland_request.request('get', pilot_url, retries=1)
        pilot_data = json.loads(resp.content)
        yield pilot_data['homeworld']

def get_planets_from_films(urls):
    for film_url in urls:
        resp = kaufland_request.request('get', film_url, retries=1)
        film_data = json.loads(resp.content)
        for planet_url in film_data['planets']:
            yield planet_url

def get_planets_from_starship(starship_data):
    planets = []
    planets.extend(list(get_planets_from_pilots(starship_data['pilots'])))
    planets.extend(list(get_planets_from_films(starship_data['films'])))
    for planet_url in set(planets):
        resp = kaufland_request.request('get', planet_url, retries=1)
        planet_data = json.loads(resp.content)
        yield planet_data['name']

starships = get_starship_from_name('Naboo')
# for starship_data in starships:
#     planets = (starship_data['name'], get_planets_from_starship(starship_data))

print({starship_data['name']: list(get_planets_from_starship(starship_data)) for starship_data in starships })

# app = Flask(__name__)
# api = Api(app)

# class StarWars(Resource):
#     def get(self):
#         return {'tste': 'starship'}, 200

# api.add_resource(StarWars, '/star-wars')

# if __name__ == '__main__':
#     app.run()  # run our Flask app

# # conn = HTTPConnection()
# # teste = conn.request('get', 'http://swapi.dev/api/planets/1/')
# # print(teste)