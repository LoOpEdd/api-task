from app.kaufland_models import HTTPConnection
import json
import datetime
import calendar

from astral import LocationInfo
from astral.sun import sun
from dateutil import tz

# TIMEZONE = 'GMT-3'
kaufland_request = HTTPConnection()

def get_city_links(name, exact_match):
    url = 'https://api.teleport.org/api/cities/'
    query = {
        'search': name
    }
    resp = kaufland_request.request('get', url, params=query, retries=1)
    cities = json.loads(resp.content)
    for city in cities['_embedded']['city:search-results']:
        if exact_match:
            if any(filter(lambda x: name in x['name'].split(',')[0][:len(name)], city['matching_alternate_names'])):
                yield city['_links']['city:item']['href']
        else:
            yield city['_links']['city:item']['href']

def get_city_data(name, exact_match):
    for city_url in get_city_links(name, exact_match):
        resp = kaufland_request.request('get', city_url, retries=1)
        yield json.loads(resp.content)

def get_sunrises(city_data, year, estimation=None):
    dates_ranges = []
    if estimation:
        est_sunrise_top, est_sunrise_low = estimation
        dates_ranges.append((est_sunrise_top - datetime.timedelta(days=4), est_sunrise_top + datetime.timedelta(days=4)))
        dates_ranges.append((est_sunrise_low - datetime.timedelta(days=4), est_sunrise_low + datetime.timedelta(days=4)))
    else:
        dates_ranges.append((datetime.date(year, 1, 1), datetime.date(year, 12, 31)))

    sunrise_top = datetime.datetime.strptime('1000-01-01 12:00:00 AM', '%Y-%m-%d %I:%M:%S %p')
    sunrise_low = datetime.datetime.strptime('9999-01-01 12:00:00 PM', '%Y-%m-%d %I:%M:%S %p')
    url = 'https://api.sunrisesunset.io/json'
    # date = datetime.date(year, 1, 1)
    # for i in range(365 + calendar.isleap(year)):
    for date_range in dates_ranges:
        current_date, final_date = date_range
        while current_date <= final_date:
            current_date_string = datetime.datetime.strftime(current_date, '%Y-%m-%d')
            query = {
                'lat': city_data['location']['latlon']['latitude'],
                'lng': city_data['location']['latlon']['longitude'],
                'timezone': city_data['_links']['city:timezone']['name'],
                'date': current_date_string
            }
            resp = kaufland_request.request('get', url, params=query, retries=1)
            data = json.loads(resp.content)
            sunrise = datetime.datetime.strptime(f"{current_date_string} {data['results']['sunrise']}", '%Y-%m-%d %I:%M:%S %p')
            if sunrise.time() > sunrise_top.time():
                sunrise_top = sunrise
            if sunrise.time() < sunrise_low.time():
                sunrise_low = sunrise
            current_date = current_date + datetime.timedelta(days=1)
    return sunrise_top, sunrise_low

def get_time_diff(time_a, time_b):
    date_time_a = datetime.datetime.combine(datetime.date.today(), time_a.time())
    date_time_b = datetime.datetime.combine(datetime.date.today(), time_b.time())
    date_time_difference = date_time_a - date_time_b
    return date_time_difference.total_seconds()

def get_estimated_sunrise(city_data, year):
    brl = tz.gettz(city_data['_links']['city:timezone']['name'])
    city = LocationInfo('', '', city_data['_links']['city:timezone']['name'], city_data['location']['latlon']['latitude'], city_data['location']['latlon']['longitude'])

    sunrise_top = datetime.datetime.strptime('1000-01-01 12:00:00 AM', '%Y-%m-%d %I:%M:%S %p')
    sunrise_low = datetime.datetime.strptime('9999-01-01 12:00:00 PM', '%Y-%m-%d %I:%M:%S %p')
    data = datetime.date(year, 1, 1)
    for i in range(365 + calendar.isleap(year)):
        try:
            s = sun(city.observer, date=data, tzinfo=brl)
        except:
            pass
        sunrise = s['sunrise']
        if sunrise.time() > sunrise_top.time():
            sunrise_top = sunrise
        if sunrise.time() < sunrise_low.time():
            sunrise_low = sunrise
        data = data + datetime.timedelta(days=1)
    return sunrise_top, sunrise_low

def get_sunrises_diff(cities_data, year, estimate):
    result = {}
    for city_data in cities_data:
        estimation = None
        if estimate:
            estimation = get_estimated_sunrise(city_data, year)
        sunrise_top, sunrise_low = get_sunrises(city_data, year, estimation)
        sunrise_diff = get_time_diff(sunrise_top, sunrise_low)
        result[city_data['full_name']] = {
            'sunrise_top': datetime.datetime.strftime(sunrise_top, '%Y-%m-%d %I:%M:%S %p'),
            'sunrise_low': datetime.datetime.strftime(sunrise_low, '%Y-%m-%d %I:%M:%S %p'),
            'sunrise_diff': sunrise_diff
        }
    return result