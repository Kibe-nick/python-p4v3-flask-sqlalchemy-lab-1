# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Updated view for individual Earthquake by ID
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    earthquake = db.session.get(Earthquake, id)  # Updated line

    if earthquake:
        response = {
            'id': earthquake.id,
            'location': earthquake.location,
            'magnitude': earthquake.magnitude,
            'year': earthquake.year
        }
        return make_response(jsonify(response), 200)
    else:
        error_response = {
            'message': f'Earthquake {id} not found.'
        }
        return make_response(jsonify(error_response), 404)

# View for Earthquakes by Magnitude
@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    response = {
        'count': len(quakes),
        'quakes': [{
            'id': quake.id,
            'location': quake.location,
            'magnitude': quake.magnitude,
            'year': quake.year,
        } for quake in quakes]
    }

    return make_response(jsonify(response), 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
