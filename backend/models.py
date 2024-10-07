from backend import db,loginManager
from flask_login import UserMixin



@loginManager.user_loader
def load_user(email_address):
    return Rent_User.query.get(str(email_address))


class Rent_User(db.Model, UserMixin):
    __tablename__ = 'user'  
    id = db.Column(db.Integer(), primary_key=True)
    phone_number = db.Column(db.String(15), unique=True, nullable=True)
    name = db.Column(db.String(length=30), nullable=True)
    experience = db.Column(db.Integer, nullable=True)
    location = db.Column(db.String(length=50), nullable=True)
    aadhar_number = db.Column(db.String(length=12), nullable=True, unique=True)
    email_address = db.Column(db.String(length=50), nullable=True, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=True)
    service = db.Column(db.String(100), nullable=True)
    Sdescription = db.Column(db.String(100), nullable=True)  
    Srating = db.Column(db.Integer, nullable=True)
    product = db.Column(db.String(100), nullable=True)
    Pimage = db.Column(db.LargeBinary, nullable=True)  
    Pvideo = db.Column(db.LargeBinary, nullable=True)
    Pdescription = db.Column(db.String(100), nullable=True)  
    Price = db.Column(db.Integer, nullable=True)  
    PDOP = db.Column(db.String(100), nullable=True)  
    Phourly_rate = db.Column(db.Integer, nullable=True)  

    data = db.relationship('Data', backref='owned_user', lazy=True)

class Data(db.Model):
    __tablename__ = 'data' 
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))  
    def __repr__(self):
        return f'Hello, {self.name}'
    
@loginManager.user_loader
def load_user(email_address):
    return Customer.query.get(str(email_address))

class Customer(db.Model, UserMixin):
    __tablename__ = 'cust'  
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    phone_number = db.Column(db.String(length=15), nullable=False)
    location = db.Column(db.String(length=50), nullable=False)
    aadhar_number = db.Column(db.String(length=12), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    Rel = db.relationship('CustData', backref='owned_user', lazy=True)

class CustData(db.Model):
    __tablename__ = 'Rel'  
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('cust.id'))  

    def __repr__(self):
        return f'Hello, {self.name}'
