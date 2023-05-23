from kaufland import HTTPConnection
from flask  import Flask
from flask_restful import Resource, Api, reqparse
import json

kaufland_request = HTTPConnection()

def get_starship_from_name(name, exact_match):
    url = f'https://swapi.dev/api/starships/'
    query = {
        'search': name
    }
    while url:
        resp = kaufland_request.request('get', url, params=query, retries=1)
        starship_data = json.loads(resp.content)
        if exact_match:
            ship = filter(lambda x: x['name'] == name, starship_data['results'])
        else:
            ship = starship_data['results']
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

# starships = get_starship_from_name('Naboo', True)

# print({starship_data['name']: list(get_planets_from_starship(starship_data)) for starship_data in starships })
