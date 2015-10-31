from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta
from sqlalchemy.ext.declarative import DeclarativeMeta
import json

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
	birthdate = db.Column(db.Date)
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
		self.birthdate = datetime.strptime(birthdate, "%d/%m/%Y").strftime("%Y-%m-%d")
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

class room(db.Model):
	__tablename__ = "room"
	id = db.Column(db.Integer, primary_key = True)
	corridor = db.Column(db.String(10))
	floor = db.Column(db.Integer)
	building = db.Column(db.String(25))
	room = db.Column(db.String(10))
	category = db.Column(db.String(25))

	def __init__(self, corridor, floor, building, room, category):
		self.corridor = corridor
		self.floor = floor
		self.building = building
		self.room = room
		self.category = category

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

	@classmethod
	def getType(self, type):
		if type == 1:
			return "Visita Medica"
		if type == 2:
			return 'Visita da Enfermagem'
		if type == 3:
			return 'Emergencia'
		if type == 4:
			return 'Visita Especialista'

	@property
	def serialize(self):
		return {
				'id': self.id,
				'idRoom': self.idRoom,
				'idUser': self.idUser,
				'idPatient': self.idPatient,
				'date': str(self.date),
				'time': str(self.time),
				'type' : self.getType(self.type),
				'idVSTemperature' : self.idVSTemperature,
				'idVSHeartbeat' : self.idVSHeartbeat,
		}


	def __init__(self, description, idRoom, idVSTemp, idVSHeart, idPatient, idUser):
		self.description = description
		self.date = datetime.now().date()
		self.time = datetime.now().time()
		self.idRoom = idRoom
		self.idVSTemperature = idVSTemp
		self.idVSHeartbeat = idVSHeart
		self.idPatient = idPatient
		self.idUser = idUser

class records(db.Model):
	__tablename__ = "records"
	id = db.Column(db.Integer, primary_key = True)
	idRoom = db.Column(db.Integer)
	idUser = db.Column(db.Integer)
	idPatient = db.Column(db.Integer)
	idMedicament =  db.Column(db.Integer)
	idEvent = db.Column(db.Integer)
	description = db.Column(db.String(250))
	dose = db.Column(db.Integer)
	unitMeasure = db.Column(db.String(5))


	def updateRecord(self, id, idRoom, uid, idPatient, idMedicament, description, dose, unitMeasure, idEvent):
		self.id = id
		self.idEvent = idEvent
		self.description = description
		self.idUser = uid
		self.idPatient = idPatient
		self.idRoom = idRoom
		self.unitMeasure = unitMeasure
		self.idMedicament = idMedicament
		self.dose = dose


	@property
	def serialize(self):
		return {
				'id': self.id,
				'idRoom': self.idRoom,
				'idUser': self.idUser,
				'idPatient': self.idPatient,
				'idMedicament': self.idMedicament,
				'idEvent': self.idEvent,
				'description' : self.description,
				'dose': self.dose,
				'unitMeasure': self.unitMeasure,
				'namePatient': self.getPatientName(self.idPatient),
		}

	def getPatientName(self, idPatient):
		p = Profile.query.filter_by(uid = idPatient).first()
		return p.firstname + " " + p.lastname

	def __init__(self, idRoom, idDoctor, idPatient, idMedicament, description, dose, unitMea, idEvent):
		self.idRoom = idRoom
		self.idUser = idDoctor
		self.idPatient = idPatient
		self.idMedicament = idMedicament
		self.idEvent = idEvent
		self.description = description
		self.dose = dose
		self.unitMeasure = unitMea

class dashboard(Profile):
	def __init__(self, name, lastname, heartbeat, temperature, age, patientID):
		self.name = name + " " + lastname
		self.heartbeat = heartbeat
		self.temperature = temperature
		self.age = self.calculate_age(age)
		self.criticHeart = self.define_critic_heartbeat(heartbeat)
		self.criticTemp = self.define_critic_temperature(temperature)
		self.criticNoSensor = self.define_critic_no_sensor(patientID)
		self.idPatient = patientID

	@property
	def serialize(self):
		return {
				'name': self.name,
				'heartbeat': self.heartbeat,
				'temperature': self.temperature,
				'age': self.age,
				'criticHeart': self.criticHeart,
				'criticTemp': self.criticTemp,
				'id' : self.idPatient,
				'criticSensor': self.criticNoSensor,
		}

	def calculate_age(self, born):
		today = date.today()
		return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

	def define_critic_heartbeat(self, heartbeat):
		if (heartbeat < 60) or (heartbeat > 100):
			return True
		else:
			return False

	def define_critic_no_sensor(self, iid):
		lastheartBeat = Heartbeat.query.filter(Heartbeat.idPatient == iid, Heartbeat.vitalSign == "Heartbeat").order_by(VitalSign.dateConsulting.desc()).first()
		total = datetime.now() - lastheartBeat.dateConsulting
		if total > timedelta(seconds=15):
			return True
		else:
			lastTemperature = Temperature.query.filter(Temperature.idPatient == iid, Temperature.vitalSign == "Temperature").order_by(VitalSign.dateConsulting.desc()).first()
			total = lastTemperature.dateConsulting - datetime.now()

			if total > timedelta(seconds=15):
				return True
			else:
				return False

	def define_critic_temperature(self, temperature):
		if (temperature < 36) or (temperature > 37.5):
			return True
		else:
			return False


class medicamentType(db.Model):
	__tablename__ = "medicamenttype"
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100))
	description = db.Column(db.String(200))
	label = db.Column(db.String(60))

	def __init__(self, name, description, label):
		self.name = name
		self.description = description
		self.label = label

class medicament(db.Model):
	__tablename__ = "medicament"
	id = db.Column(db.Integer, primary_key = True)
	description = db.Column(db.String(30))
	type = db.Column(db.Integer)

	def __init__(self, desc, type):
		self.description = desc
		self.type = type