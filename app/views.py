from app import app
from flask_restx import Resource, Api, reqparse, inputs
from app.starwars_models import get_starship_from_name, get_planets_from_starship
from app.sunrise_models import get_city_data, get_sunrises_diff

api = Api(
    app,
    version='1.0',
    title='Kaufland API',
    description='The goal of this task is to create a reliable python HTTP-based API client. The API endpoint given in the task is taken from the OpenAPI database and offers data that is not significant to Kaufland, but includes the same general requirements used in any proprietary API endpoint and therefore is a good sandbox for client application development.',
    contact_email='felipelopesxavier@gmail.com',
    default='Kaufland'
)

# StarWars ---------------------------------------------------------------
ns_starwars = api.namespace('starwars', description='Starwars API.')

starwars_parser = reqparse.RequestParser()
starwars_parser.add_argument('name', type=str, required=True, help='Name of the starship.')
starwars_parser.add_argument('exact_match', type=inputs.boolean, help='If it has to be an exact match.')

@ns_starwars.route('/starship_planets')
class StarWars(Resource):
    @ns_starwars.doc(parser=starwars_parser)
    def get(self):
        args = starwars_parser.parse_args()
        name = args['name']
        exact_match = args['exact_match']
        starships = get_starship_from_name(name, exact_match)
        return {starship_data['name']: list(get_planets_from_starship(starship_data)) for starship_data in starships}

sunrise_parser = reqparse.RequestParser()
sunrise_parser.add_argument('name', type=str, required=True, help='Name of the city.')
sunrise_parser.add_argument('year', type=int, required=True, help='Year desired.')
sunrise_parser.add_argument('estimate', type=inputs.boolean, required=True, help='Get the date range values to get sunrise based on an estimation.')
sunrise_parser.add_argument('exact_match', type=inputs.boolean, help='If it has to be an exact match.')

# Sunrise ---------------------------------------------------------------
ns_sunrise = api.namespace('sunrise', description='Sunrise API.')

@ns_sunrise.route('/sunrise_diff')
class Sunrise(Resource):
    @api.doc(description='''
        Gets the difference between the earliest and the latest sunrise during the input year for a given city.
        If estimate is True, it will estimate the earliest and the latest sunrise, and then will generate a date range to gatter data from the https://sunrisesunset.io/api/.
    ''')
    @ns_sunrise.doc(parser=sunrise_parser)
    def get(self):
        args = sunrise_parser.parse_args()
        name = args['name']
        year = args['year']
        estimate = args['estimate']
        exact_match = args['exact_match']
        return get_sunrises_diff(get_city_data(name, exact_match), year, estimate)