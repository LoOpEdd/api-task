from kaufland import HTTPConnection
from flask  import Flask
from flask_restful import Resource, Api, reqparse
import json
from datetime import datetime, timedelta, date
import calendar

kaufland_request = HTTPConnection()

def get_city_links(name):
    url = 'https://api.teleport.org/api/cities/'
    query = {
        'search': name
    }
    resp = kaufland_request.request('get', url, params=query, retries=1)
    cities = json.loads(resp.content)
    for city in cities['_embedded']['city:search-results']:
        yield city['_links']['city:item']['href']

def get_city_data(name):
    for city_url in get_city_links(name):
        resp = kaufland_request.request('get', city_url, retries=1)
        yield json.loads(resp.content)

def get_sunrise(city_data, year):
    sunrise_top = datetime.strptime('1000-01-01 12:00:00 AM', '%Y-%m-%d %I:%M:%S %p')
    sunrise_low = datetime.strptime('9999-01-01 12:00:00 PM', '%Y-%m-%d %I:%M:%S %p')
    url = 'https://api.sunrisesunset.io/json'
    date_str = f'{year}-01-01'
    for i in range(365 + calendar.isleap(year)):
        query = {
            'lat': city_data['location']['latlon']['latitude'],
            'lng': city_data['location']['latlon']['longitude'],
            'timezone': 'GMT-3',
            'date': date_str,
        }
        resp = kaufland_request.request('get', url, params=query, retries=1)
        data = json.loads(resp.content)
        sunrise = datetime.strptime(f"{date_str} {data['results']['sunrise']}", '%Y-%m-%d %I:%M:%S %p')
        if sunrise.time() > sunrise_top.time():
            sunrise_top = sunrise
        if sunrise.time() < sunrise_low.time():
            sunrise_low = sunrise
        date_str = datetime.strftime(datetime.strptime(date_str, '%Y-%m-%d') + timedelta(days=1), '%Y-%m-%d')
    return sunrise_top, sunrise_low

def get_time_diff(time_a, time_b):
    date_time_a = datetime.combine(date.today(), time_a.time())
    date_time_b = datetime.combine(date.today(), time_b.time())
    date_time_difference = date_time_a - date_time_b
    return date_time_difference.total_seconds()

for city_data in get_city_data('Curitiba'):
    sunrise_top, sunrise_low = get_sunrise(city_data, 2023)
    print({
        'name': city_data['full_name'],
        'diff': get_time_diff(sunrise_top, sunrise_low)
    })