from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from datetime import datetime
import uuid
from flask_marshmallow import Marshmallow

#internal imports
from .helpers import get_image

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    """
    Given *user_id*, retrun the associated User object.

    :param unicode user_ud: user_id (email) user to retrieve
    """
    
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    user_id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())


    def __init__(self, username, email, password, first_name="", last_name=""):
        self.user_id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = self.set_password(password)

    
    def set_id(self):
        return str(uuid.uuid4())
    
    def get_id(self):
        return str(self.user_id)
    
    def set_password(self, password):
        return generate_password_hash(password)
    
    def __repr__(self):
        return f"<User: {self.username}>"
    

class Weapon(db.Model):
    weap_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String)
    description = db.Column(db.String(200))
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default = datetime.utcnow())

    def __init__(self, name, price, quantity, image="", description=""):
        self.weap_id = self.set_id()
        self.name = name
        self.image = self.set_image(image, name)
        self.description = description
        self.price = price
        self.quantity = quantity

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_image(self, image, name):
        print('image', image)
        if not image:
            print("We don't have an image")
            image = get_image(name)

        return image
    
    def decrement_quantity(self, quantity):
        self.quantity -= int(quantity)
        return self.quantity
    
    def increment_quantity(self, quantity):
        self.quantity += int(quantity)
        return self.quantity
    
    def __repr__(self):
        return f"<Weapon: {self.name}>"
    


class WeaponSchema(ma.Schema):
    class Meta:
        fields = ['weap_id', 'name', 'image', 'description', 'price', 'quantity']

weapon_schema = WeaponSchema()
weapons_schema = WeaponSchema(many=True)
