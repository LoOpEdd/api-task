from flask import Flask
from flask_restx import Resource, Api, reqparse
from starwars import get_starship_from_name

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, help='Name of the starship')
parser.add_argument('exact_match', type=bool, help='If it has to be an exact match')

@api.route('/starwars/')
class StarWars(Resource):
    @api.doc(parser=parser)
    def get(self):
        args = parser.parse_args()
        post_var1 = args['name']
        post_var2 = args['exact_match']

        return {post_var1: post_var2}

if __name__ == '__main__':
    app.run(debug=True)