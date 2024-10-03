from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#class User(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    email = db.Column(db.String(120), unique=True, nullable=False)
#    password = db.Column(db.String(80), unique=False, nullable=False)
#    is_active = db.Column(db.Boolean(), unique=False, nullable=False)


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), nullable=False)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(6), nullable=False, unique=True)


class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    birth_year = db.Column(db.Integer)
    gender = db.Column(db.String(25))

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    climate = db.Column(db.String(25))
    population = db.Column(db.Integer)


class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    User_from_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_from = relationship(Users) 
    fav_planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    fav_planets = relationship(Planets)
    fav_characters_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    fav_planets = relationship(Characters)


    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }