from flask.ext.wtf import Form
from wtforms.fields import TextField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from models import db, User

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