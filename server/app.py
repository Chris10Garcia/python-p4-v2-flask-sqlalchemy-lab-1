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

# Add views here

@app.route("/earthquakes/<int:id>")
def earthquakeID(id):
    earthquake = Earthquake.query.filter(Earthquake.id == id).first()

    if not earthquake:
        return {"message": f"Earthquake {id} not found."}, 404

    response = make_response(
        earthquake.to_dict(),
        200
    )

    return response

@app.route("/earthquakes/magnitude/<float:magnitude>")
def earthquakeByMagnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    count = len(earthquakes)

    earthquakes_serialized = [earthquake.to_dict() for earthquake in earthquakes]

    response = make_response(
        jsonify({"count": count, "quakes" : earthquakes_serialized }),
        200
    )

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
