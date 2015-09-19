from flask.ext.wtf import Form
from wtforms.fields import TextField, TextAreaField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired
from models import db, User, Profile

class ContactForm(Form):
	name = TextField("Name",  validators=[DataRequired("Please enter your name.")])
	email = TextField("Email",  validators=[DataRequired("Please enter your email address.")])
	subject = TextField("Subject",  validators=[DataRequired("Please enter a subject.")])
	message = TextAreaField("Message",  validators=[DataRequired("Please enter a message.")])
	submit = SubmitField("Send")
  	  
class SigninForm(Form):
	email = TextField("Email",  validators=[DataRequired("Please enter your email address.")])
	password = PasswordField('Password', validators=[DataRequired("Please enter a password.")])
	submit = SubmitField("Sign In")
   
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
	myRoles = [('1', ('Medico(a)')), ('2', ('Enfermeiro(a)')), ('3', ('Administrador(a)'))]
	role = SelectField(u'Papel', choices = myRoles, validators=[DataRequired("Por favor informe o papel")])
	myBloodTypes = [('1', ('A+')), ('2', ('B+')), ('3', ('AB+')), ('4', ('O+')), ('5', ('A-')), ('6', ('B-')), ('7', ('AB-')), ('8', ('O-'))]
	bloodType = SelectField(u'Tipo Sanguineo', choices = myBloodTypes, validators=[DataRequired("Por favor informe o tipo sanguineo")])
	submit = SubmitField("SALVAR")

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False
