from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()
 
class User(db.Model):
	__tablename__ = 'users'
	uid = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(120), unique=True)
	pwdhash = db.Column(db.String(54))
	rfid = db.Column(db.String(50))
	def __init__(self, email, password):
		self.email = email.lower()
		self.set_password(password)
     
	def set_password(self, password):
		self.pwdhash = generate_password_hash(password)
   
	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)

class Profile(db.Model):
	__tablename__ = 'profile'
	uid = db.Column(db.Integer, primary_key = True)
	firstname = db.Column(db.String(50))
	lastname = db.Column(db.String(80))
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

	def __init__(self, id, firstname, lastname, cpf, birthdate, rg, address, number, additionalInformation, district, region, country, telephone, cellphone, profileType, role, bloodType):
		self.id = id
		self.firstname = firstname
		self.lastname = lastname
		self.cpf = cpf
		self.birthdate = birthdate
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

class Patients(Profile):

	def __init__(self, id, firstname, lastname, cpf, rg, address, number, additionalInformation, district, region, country, telephone, cellphone, profileType, bloodType):
		role = "Paciente"
		Profile.__init__(self, id, firstname, lastname, cpf, rg, address, number, additionalInformation, district, region, country, telephone, cellphone, profileType, role, bloodType)

class VitalSign(db.Model):
	__tablename__ = 'VitalSign'
	id = db.Column(db.Integer, primary_key = True)
	idPatient = db.Column(db.Integer)
	vitalSign = db.Column(db.String(30))
	value = db.Column(db.Float)
	dateConsulting = db.Column(db.DateTime)

	def __init__(self, patientId, vitalSign, value, dateConsulting):
		self.idPatient = patientId
		self.dateConsulting = dateConsulting
		self.value = value
		self.vitalSign = vitalSign

class Temperature(VitalSign):

	def __init__(self, patientId, value):
		self.idPatient = patientId
		self.value = value
		self.vitalSign = "Temperature"
		self.dateConsulting = datetime.now()

class Heartbeat(VitalSign):

	def __init__(self, patientId, value):
		self.idPatient = patientId
		self.value = value
		self.vitalSign = "Heartbeat"
		self.dateConsulting = datetime.now()

class event(db.Model):
	__tablename__ = "event"
	id = db.Column(db.Integer, primary_key = True)
	description = db.Column(db.String(60))
	date = db.Column(db.DateTime)
	time = db.Column(db.DateTime)
	type = db.Column(db.Integer)
	idRoom = db.Column(db.Integer)
	idUser = db.Column(db.Integer)
	idVSTemperature = db.Column(db.Integer)
	idVSHeartbeat = db.Column(db.Integer)
	idPatient = db.Column(db.Integer)

	def __init__(self, description, idRoom, idVSTemp, idVSHeart, idPatient, idUser):
		self.description = description
		self.date = datetime.now().date()
		self.time = datetime.now().time()
		self.idRoom = idRoom
		self.idVSTemperature = idVSTemp
		self.idVSHeartbeat = idVSHeart
		self.idPatient = idPatient
		self.idUser = idUser
