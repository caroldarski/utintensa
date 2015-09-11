from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
 
db = SQLAlchemy()
 
class User(db.Model):
	__tablename__ = 'users'
	uid = db.Column(db.Integer, primary_key = True)
	firstname = db.Column(db.String(100))
	lastname = db.Column(db.String(100))
	email = db.Column(db.String(120), unique=True)
	pwdhash = db.Column(db.String(54))
   
	def __init__(self, firstname, lastname, email, password):
		self.firstname = firstname.title()
		self.lastname = lastname.title()
		self.email = email.lower()
		self.set_password(password)
     
	def set_password(self, password):
		self.pwdhash = generate_password_hash(password)
   
	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)
	
class Profile(db.Model):
	__tablename__ = 'profile'
	uid = db.Column(db.Integer, primary_key = True)
	birthdate = db.Column(db.DateTime)
	cpf = db.Column(db.String(11))
	rg = db.Column(db.String(10))
	address = db.Column(db.String(60))
	number = db.Column(db.Integer)
	additionalInformation = db.Column(db.String(20))
	district = db.Column(db.String(20))
	region = db.Column(db.String(2))
	country = db.Column(db.String(2))
	telephone = db.Column(db.String(20))
	cellphone = db.Column(db.String(20))
	profileType = db.Column(db.String(1))
	role = db.Column(db.String(20))
	bloodType = db.Column(db.String(3))

	def __init__(self, id, cpf, rg, address, number, additionalInformation, district, region, country, telephone, cellphone, profileType, role, bloodType):
		self.id = id
		self.cpf = cpf
		self.rg = rg
		self.address = address
		self.number = number
		self.additionalInformation = additionalInformation
		self.district = district
		self.region = region
		self.country = country
		self.telephone = telephone
		self.cellphone = cellphone
		self.profileType = profileType
		self.role = role
		self.bloodType = bloodType
	
	def updateData(self, id, cpf, rg, address, number, additionalInformation, district, region, country, telephone, cellphone, profileType, role, bloodType):
		self.id = id
		self.cpf = cpf
		self.rg = rg
		self.address = address
		self.number = number
		self.additionalInformation = additionalInformation
		self.district = district
		self.region = region
		self.country = country
		self.telephone = telephone
		self.cellphone = cellphone
		self.profileType = profileType
		self.role = role
		self.bloodType = bloodType
