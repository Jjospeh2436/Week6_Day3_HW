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
    
class Customer(db.Model):
    cust_id = db.Column(db.String, primary_key=True)
    date_created = db.Column(db.String, default = datetime.utcnow())
    weapord = db.relationship('WeapOrder', backref = 'customer', lazy=True)

    def __init__(self, cust_id):
        self.cust_id = cust_id

    def __repr__(self):
        return f"<Customer: {self.cust_id}>"
    

class WeapOrder(db.Model):
    weaporder_id = db.Column(db.String, primary_key=True)
    weap_id = db.Column(db.String, db.ForeignKey('weapon.weap_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable = False)
    price = db.Column(db.Numeric(precision = 10, scale = 2), nullable=False)
    order_id = db.Column(db.String, db.ForeignKey('order.order_id'), nullable=False)
    cust_id = db.Column(db.String, db.ForeignKey('customer.cust_id'), nullable=False)

    def __init__(self, weap_id, quantity, price, order_id, cust_id):
        self.weaporder_id = self.set_id()
        self.weap_id = weap_id
        self.quantity = quantity
        self.price = price
        self.order_id = order_id
        self.cust_id = cust_id


    def set_id(self):
        return str(uuid.uuid4())
    
    def set_price(self, quantity, price):
        quantity = int(quantity)
        price = float(price)

        self.price = quantity * price
        return self.price
    
    def update_quantity(self, quantity):
        self.quantity = int(quantity)
        return self.quantity
    

class Order(db.Model):
    order_id = db.Column(db.String, primary_key=True)
    order_total = db.Column(db.Numeric(precision=10, scale=2), nullable =False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow())
    weapord = db.relationship('WeapOrder', backref = 'order', lazy=True)

    def __init__(self):
        self.order_id = self.set_id()
        self.order_total = 0.00

    def set_id(self):
        return str(uuid.uuid4())
    
    def increment_ordertotal(self, price):
        self.order_total = float(self.order_total)
        self.order_total += float(price)

        return self.order_total
    
    def decrement_ordertotal(self, price):
        self.order_total = float(self.order_total)
        self.order_total -= float(price)

        return self.order_total
    
    def __repr__(self):
        return f"<Order: {self.order_id}>"

class WeaponSchema(ma.Schema):
    class Meta:
        fields = ['weap_id', 'name', 'image', 'description', 'price', 'quantity']

weapon_schema = WeaponSchema()
weapons_schema = WeaponSchema(many=True)
