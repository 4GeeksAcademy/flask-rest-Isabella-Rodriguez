"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planets, FavoritesCharacters,FavoritesPlanets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_users():
    all_user = list(User.query.all())
    results = list(map(lambda user: user.serialize(), all_user)) 
   
    return jsonify(results), 200

@app.route('/people', methods=['GET'])
def get_characters():
    all_characters = list(Characters.query.all()) 
    results = list(map(lambda character: character.serialize(), all_characters)) 

    return jsonify(results), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_character(people_id):
    character = Characters.query.filter_by(id=people_id).first()
    
    if character is None:
        return jsonify({"error": "Personaje no encontrado"}), 404
    
    return jsonify(character.serialize()), 200


@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets = list(Planets.query.all()) 
    results = list(map(lambda planet: planet.serialize(), all_planets)) 

    return jsonify(results), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.filter_by(id=planet_id).first()
    
    if planet is None:
        return jsonify({"error": "Planeta no encontrado"}), 404
    
    return jsonify(planet.serialize()), 200


@app.route('/planets/<int:planet_id>', methods=['POST'])
def add_planet(planet_id):
    body = request.get_json()
    favorite = FavoritesPlanets(user_id = body['user_id'], favorite_planet = body['favorite_planet'])
    db.session.add(favorite)
    db.session.commit()

    response_body = {
        "msg": "se agrego a Favoritos "
    }
    
    return jsonify(response_body), 200

@app.route('/characters/<int:people_id>', methods=['POST'])
def add_character(people_id):
    body = request.get_json()
    favorite = FavoritesCharacters(user_id = body['user_id'], favorite_character = body['favorite_character'])
    db.session.add(favorite)
    db.session.commit()

    response_body = {
        "msg": "se agrego a Favoritos "
    }
    
    return jsonify(response_body), 200

@app.route('/user/favorites/<int:id_user>', methods=['GET'])
def get_favorites(id_user):
    
    favorites_planets = FavoritesPlanets.query.filter_by(user_id=id_user)
    planets = list(map(lambda item: item.serialize(), favorites_planets)) 

    favorites_characters = favorites_characters.query.filter_by(user_id=id_user)
    characters = list(map(lambda item: item.serialize(), favorites_characters))

    result = {
        "fav_planets": planets,
        "fav_characters": characters
    }


    return jsonify(result), 200

@app.route('/planets/<int:planet_id>/<int:id_user>', methods=['DELETE'])
def delete_planeta(planet_id, id_user):
    favorites_planets = FavoritesPlanets.query.filter_by(user_id=id_user).all()

    def planet_to_delete(item):
        return item.favorite_planet == planet_id
    
    seleccion_de_planeta = list(filter(planet_to_delete, favorites_planets))

    if len(seleccion_de_planeta) > 0:
        planeta_a_eliminar = seleccion_de_planeta[0]
        db.session.delete(planeta_a_eliminar)
        db.session.commit()

        response_body = {"msg": "Se eliminó correctamente"}
    else:
        response_body = {"msg": "No se encontró el planeta favorito o el usurio"}

    return jsonify(response_body), 200

@app.route('/people/<int:people_id>/<int:id_user>', methods=['DELETE'])
def delete_character(people_id, id_user):
    favorites_characters = FavoritesCharacters.query.filter_by(user_id=id_user).all()

    def character_to_delete(item):
        return item.favorite_character == people_id
    
    seleccion_de_personaje = list(filter(character_to_delete, favorites_characters))

    if len(seleccion_de_personaje) > 0:
        personaje_a_eliminar = seleccion_de_personaje[0]
        db.session.delete(personaje_a_eliminar)
        db.session.commit()

        response_body = {"msg": "Se eliminó correctamente"}
    else:
        response_body = {"msg": "No se encontró el personaje favorito o el usuario"}

    return jsonify(response_body), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)