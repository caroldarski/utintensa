from flask.ext.wtf import Form
from wtforms.fields import TextField, TextAreaField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired
from models import db, User, Profile, medicamentType, room, medicament

class ContactForm(Form):
	name = TextField("Name",  validators=[DataRequired("Please enter your name.")])
	email = TextField("Email",  validators=[DataRequired("Please enter your email address.")])
	subject = TextField("Subject",  validators=[DataRequired("Please enter a subject.")])
	message = TextAreaField("Message",  validators=[DataRequired("Please enter a message.")])
	submit = SubmitField("Send")
  	  
class SigninForm(Form):
	email = TextField("Email",  validators=[DataRequired("Please enter your email address.")])
	password = PasswordField('Password', validators=[DataRequired("Please enter a password.")])
	submit = SubmitField("Entrar")
   
	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
 
	def validate(self):
		if not Form.validate(self):
			return False
     
		user = User.query.filter_by(email = self.email.data.lower()).first()
		if user and user.check_password(self.password.data):
			return True
		else:
			self.email.errors.append("Invalid e-mail or password")
			return False

class ProfileForm(Form):
	birthDate = TextField("Data de Nascimento")
	cpf = TextField("CPF", validators=[DataRequired("Por favor informe seu CPF")])
	rg = TextField("RG", validators=[DataRequired("Por favor informe seu RG")])
	address = TextField("Endereco", validators=[DataRequired("Por favor informe seu endereco")])
	number = TextField("Numero", validators=[DataRequired("Por favor informe seu numero")])
	additionalInformation = TextField("Complemento")
	district = TextField("Bairro")
	region = TextField("UF", validators=[DataRequired("Por favor informe sua UF")])
	country = TextField("Pais", validators=[DataRequired("Por favor informe seu pais")])
	telephone = TextField("Telefone")
	cellphone = TextField("Celular", validators=[DataRequired("Por favor informe seu telefone celular")])
	profileType = TextField("Tipo de perfil")
	role = TextField("Cargo")
	bloodType = TextField("Tipo Sanguineo", validators=[DataRequired("Por favor informe seu tipo sanguineo")])
	uName = TextField("Usuario")
	submit = SubmitField("SALVAR")
	 
	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
 
	def validate(self):
		if not Form.validate(self):
			return False
			
	def updateHeaderData(self, p, u):
		self.role.label = "Cargo: " + p.role
		self.id = p.uid
		self.uName.label = p.firstname, " ", p.lastname


class CreatePersonForm(Form):
	firstname = TextField("Primeiro nome")
	lastname = TextField("Sobrenome", validators=[DataRequired("Por favor informe o primeiro nome")])
	birthDate = TextField("Data de Nascimento", validators=[DataRequired("Por favor informe o sobrenome")])
	cpf = TextField("CPF", validators=[DataRequired("Por favor informe seu CPF")])
	rg = TextField("RG", validators=[DataRequired("Por favor informe seu RG")])
	address = TextField("Endereco", validators=[DataRequired("Por favor informe seu endereco")])
	number = TextField("Numero", validators=[DataRequired("Por favor informe seu numero")])
	additionalInformation = TextField("Complemento")
	district = TextField("Bairro")
	region = TextField("UF", validators=[DataRequired("Por favor informe sua UF")])
	country = TextField("Pais", validators=[DataRequired("Por favor informe seu pais")])
	telephone = TextField("Telefone")
	cellphone = TextField("Celular", validators=[DataRequired("Por favor informe seu telefone celular")])
	profileType = TextField("Tipo de perfil")
	myRoles = [('Medico(a)', ('Medico(a)')), ('Enfermeiro(a)', ('Enfermeiro(a)')), ('Administrador(a)', ('Administrador(a)')), ('Paciente', ('Paciente'))]
	role = SelectField(u'Papel', choices = myRoles, validators=[DataRequired("Por favor informe o papel")])
	myBloodTypes = [('A+', ('A+')), ('B+', ('B+')), ('AB+', ('AB+')), ('O+', ('O+')), ('A-', ('A-')), ('B-', ('B-')), ('AB-', ('AB-')), ('O-', ('O-'))]
	bloodType = SelectField(u'Tipo Sanguineo', choices = myBloodTypes, validators=[DataRequired("Por favor informe o tipo sanguineo")])
	submit = SubmitField("SALVAR")

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False

class roomField(SelectField):

	def __init__(self, *args, **kwargs):
		super(roomField, self).__init__(*args, **kwargs)
		self.choices = []
		for r in room.query.all():
			self.choices.append([r.id, (r.building + " " + str(r.floor) + " " + str(r.corridor) + " " + r.room)])

class medicamentField(SelectField):

	def __init__(self, *args, **kwargs):
		super(medicamentField, self).__init__(*args, **kwargs)
		self.choices = []
		for med in medicament.query.all():
			self.choices.append([med.id, med.description])

class patientField(SelectField):

	def __init__(self, *args, **kwargs):
		super(patientField, self).__init__(*args, **kwargs)
		self.choices = []
		for p in Profile.query.filter_by(role = "Paciente").all():
			self.choices.append([p.uid, (p.firstname + " " + p.lastname)])

class CreateMedicalAppointment(Form):
	id = TextField("id")
	date = TextField("Data")
	time = TextField("Horario")
	types = [('1', ('Visita Medica')), ('2', ('Visita da Enfermagem')), ('3', ('Emergencia')), ('4', ('Visita Especialista'))]
	type = SelectField(u'Tipo de Atendimento', choices = types)
	idUser = TextField("Atendido por")
	description = TextAreaField("Descricao do atendimento")
	idRoom = roomField("Localizacao")
	idPatient = patientField("Paciente")
	idMedicament = medicamentField("Medicamento aplicado")
	dose = TextField("Dose")
	unitMeasure = TextField("Unidade de medida")
	heart = TextField("Frequencia de batimento cardiaco (b/m)")
	temp = TextField("Temperatura")

	submit = SubmitField("SALVAR")

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False

	def updateHeaderData(self, p):
		print p.lastname
		self.idUser.label = "Atendido por: " +  p.firstname + " " + p.lastname
		if self.id.data <> None:
			self.heart.label = "Frequencia de batimento cardiaco: " + str(self.heart.data) +"(b/m)"
			self.temp.label = "Temperatura: " + str(self.temp.data)
			self.date.label = "Data de Atendimento: " + str(self.date.data) + " " + str(self.time.data)
			if ( self.idPatient.data == '5' ):
				self.idPatient.label = "Paciente: Alice Maravilha"
			else:
				self.idPatient.label = "Paciente: Joao Oliveira"
		else:
			self.heart.label = "Frequencia de batimento cardiaco(b/m)"
			self.temp.label = "Temperatura"
			self.date.label = "Data"
			self.idPatient.label = "Paciente"


class CreateMedicamentType(Form):
	name = TextField("Nome")
	description = TextAreaField("Descricao")
	myLabels = [('Sem tarja', ('Sem tarja')), ('Tarja amarela', ('Tarja amarela')), ('Tarja vermelha', ('Tarja vermelha')), ('Tarja preta', ('Tarja preta'))]
	labelm = SelectField(u'Faixa', choices = myLabels, validators=[DataRequired("Por favor informe a faixa")])
	submit = SubmitField("SALVAR")

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False

class MedicamentTypeField(SelectField):

	def __init__(self, *args, **kwargs):
		super(MedicamentTypeField, self).__init__(*args, **kwargs)
		self.choices = []
		for medicament in medicamentType.query.all():
			self.choices.append([medicament.id, medicament.name])


class CreateMedicament(Form):
	type = MedicamentTypeField(u'Tipo')
	description = TextAreaField("Descricao")
	submit = SubmitField("SALVAR")

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False
