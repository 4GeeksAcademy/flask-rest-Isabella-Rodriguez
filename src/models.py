from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    last_name = db.Column(db.String(120), unique=False, nullable=False)
    user_name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    
    
    fav_planet = db.relationship('FavoritesPlanets', backref='user', lazy=True)
    fav_character = db.relationship('FavoritesCharacters', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "user_name": self.user_name,
            "email": self.email,
        }

# Personajes
class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    height = db.Column(db.String(250))
    eye_color = db.Column(db.String(250), nullable=False)
    birth_year = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)

    favorites_characters = db.relationship('FavoritesCharacters', backref='characters', lazy=True)
   

    def __repr__(self):
        return '<Personajes %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
        }


# Tabla Personajes Favoritos
class FavoritesCharacters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    favorite_character = db.Column(db.Integer, db.ForeignKey('characters.id'),
        nullable=False)
    
 

    def __repr__(self):
        return '<FavCharacters %r>' % self.id

    def serialize(self):
        return {
          "id": self.id,
          "user_id": self.user_id,
          "favorite_character": self.favorite_character
        }
    
#  Planetas
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    diameter = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250), nullable=False)
    terrain = db.Column(db.String(250), nullable=False)

    fav_planets = db.relationship('FavoritesPlanets', backref='planets', lazy=True)
    
    
    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "climate": self.climate,
            "terrain": self.terrain,
        }

# Tabla Planetas Favoritos
class FavoritesPlanets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    favorite_planet = db.Column(db.Integer, db.ForeignKey('planets.id'),
        nullable=False)
    
    

    def __repr__(self):
        return '<FavPlanets %r>' % self.user_id

    def serialize(self):
        return {
          "id": self.id,
          "user_id": self.user_id,
          "favorite_planet": self.favorite_planet
        }