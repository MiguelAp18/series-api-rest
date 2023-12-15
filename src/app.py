from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
import os

load_dotenv()
password = os.getenv('PASSWORD')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:' + password + '@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Serie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), unique=True)
    description = db.Column(db.String(100))

    def __init__(self, title, description):
        self.title = title
        self.description = description

with app.app_context():
    db.create_all()

class SerieSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description')

serie_schema = SerieSchema()
series_schema = SerieSchema(many=True)

@app.route('/series', methods=['POST'])
def create_serie():
    title = request.json['title']
    description = request.json['description']

    new_serie = Serie(title, description)
    db.session.add(new_serie)
    db.session.commit()

    return serie_schema.jsonify(new_serie)

@app.route('/series', methods=['GET'])
def get_series():
    all_series = Serie.query.all()
    result = series_schema.dump(all_series)

    return jsonify(result)

@app.route('/series/<id>', methods=['GET'])
def get_serie(id):
    serie = Serie.query.get(id)
    return serie_schema.jsonify(serie)

@app.route('/series/<id>', methods=['PUT'])
def update_serie(id):
    serie = Serie.query.get(id)

    title = request.json['title']
    description = request.json['description']

    serie.title = title
    serie.description = description

    db.session.commit()
    return serie_schema.jsonify(serie)

@app.route('/series/<id>', methods=['DELETE'])
def delete_serie(id):
    serie = Serie.query.get(id)
    db.session.delete(serie)
    db.session.commit()

    return serie_schema.jsonify(serie)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'Message': 'Welcome to the Series API!'})

if __name__ == '__main__':
    app.run(debug=True)