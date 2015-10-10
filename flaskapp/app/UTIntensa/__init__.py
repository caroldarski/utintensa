from flask import Flask
 
app = Flask(__name__)
 
app.secret_key = 'development key'
app.config["MAIL_SERVER"] = "mail.cdarski.com"
app.config["MAIL_PORT"] = 25
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'contact+cdarski.com'
app.config["MAIL_PASSWORD"] = 'testeSenha123'

from routes import mail
mail.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/development'
 
from models import db
db.init_app(app) 
 
import UTIntensa.routes
