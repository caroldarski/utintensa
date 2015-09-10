from UTIntensa import app
from flask import render_template, request, flash, session, url_for, redirect
from forms import ContactForm, SigninForm, ProfileForm
from flask.ext.mail import Message, Mail
from models import db, User, Profile
 
mail = Mail()

@app.route('/testdb')
def testdb():
  if db.session.query("1").from_statement("SELECT 1").all():
    return 'It works.'
  else:
    return 'Something is broken.'
	
@app.route('/')
def home():
  return render_template('home.html')
  
@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()
 
  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      msg = Message(form.subject.data, sender='contact@cdarski.com', recipients=['contact@cdarski.com'])
      msg.body = """
      From: %s &lt;%s&gt;
      %s
      """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)
 
      return render_template('contact.html', success=True)
 
  elif request.method == 'GET':
    return render_template('contact.html', form=form) 

@app.route('/profile', methods=['GET', 'POST'])
def profile():
  form = ProfileForm()
  
  if 'email' not in session:
    return redirect(url_for('signin'))
 
  user = User.query.filter_by(email = session['email']).first()
  profile = Profile.query.filter_by(uid = user.uid).first()
  
  if user is None:
    return redirect(url_for('signin'))
  else:
    return render_template('profile.html', form=form)
	
@app.route('/dashboard')
def dashboard():
 
  if 'email' not in session:
    return redirect(url_for('signin'))
 
  user = User.query.filter_by(email = session['email']).first()
 
  if user is None:
    return redirect(url_for('signin'))
  else:
    return render_template('dashboard.html')
	
@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()
  if 'email' in session:
	return redirect(url_for('profile'))
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('login.html', form=form)
    else:
      session['email'] = form.email.data
      return redirect(url_for('profile'))
                 
  elif request.method == 'GET':
    return render_template('login.html', form=form)

@app.route('/signout')
def signout():
  
  if 'email' not in session:
    return redirect(url_for('signin'))
     
  session.pop('email', None)
  return redirect(url_for('home'))
  
if __name__ == '__main__':
  app.run(debug=True)