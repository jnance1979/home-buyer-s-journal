from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(70))
    password = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    property = db.relationship('Property', backref = 'user', lazy='dynamic')

    def __init__(self, name, email, password):
        super().__init__()
        self.name = name
        self.email = email
        self.password = password
        self.generate_password(self.password)

    def check_password(self, password_to_check):
        return check_password_hash(self.password, password_to_check)

    def generate_password(self, password_create_salt_from):
        self.password = generate_password_hash(password_create_salt_from)

    def __repr__(self):
        return f'User: {self.email}'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(70))
    nickname = db.Column(db.String(70))
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    impressions = db.Column(db.String(500))
    pin = db.Column(db.String(30))
    dashed_pin = db.Column(db.String(30))
    taxes = db.Column(db.Float)
    payment = db.Column(db.Float)   
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, address, nickname, bedrooms, bathrooms, impressions, pin, dashed_pin, taxes, payment, user_id):
        super().__init__()
        self.address = address
        self.nickname = nickname
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.impressions = impressions
        self.pin = pin
        self.dashed_pin = dashed_pin
        self.taxes = taxes     
        self.payment = payment  
        self.user_id = user_id

    def __repr__(self):
        return f'Property: {self.address}'