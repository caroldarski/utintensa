from UTIntensa import app
from flask import render_template, request, flash, session, url_for, redirect, jsonify
from forms import ContactForm, SigninForm, ProfileForm, CreatePersonForm
from flask.ext.mail import Message, Mail
from models import db, User, Profile, Temperature, Heartbeat

mail = Mail()

@app.route('/testdb')
def testdb():
	if db.session.query("1").from_statement("SELECT 1").all():
		return 'It works.'
	else:
		return 'Something is broken.'
	
@app.route('/')
def home():
	return redirect(url_for('profile'));
  
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
	
	if 'email' not in session:
		return redirect(url_for('signin'))
  
	user = User.query.filter_by(email = session['email']).first()
	profile = Profile.query.filter_by(uid = user.uid).first()
	
	form = ProfileForm(obj=profile)
	form.updateHeaderData(profile, user)

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('profile.html', form=form)
		else:
			profile.updateData(user.uid, form.cpf.data, form.rg.data, form.address.data, int(form.number.data), form.additionalInformation.data, form.district.data, form.region.data, form.country.data, form.telephone.data, form.cellphone.data, form.profileType.data, form.role.data, form.bloodType.data)
			db.session.commit()
			return redirect(url_for('profile'))
	  
	elif request.method == "GET":  
		if user is None:
			return redirect(url_for('signin'))
		else:
			return render_template('profile.html', form=form)\

@app.route('/Sendheartbeat', methods=['POST'])
def Sendheartbeat():
    vheartbeat = request.json.get('heartbeat')
    iid = request.json.get('id')
    if vheartbeat is None or iid is None:
        abort(400)
    else:
        heartbeatOBJ = Heartbeat(iid, vheartbeat)
        db.session.add(heartbeatOBJ)
        db.session.commit()
    return jsonify({'id' : iid, 'heartbeat' : vheartbeat})

@app.route('/SendTemperature', methods=['POST'])
def SendTemperature():
    vtemperature = request.json.get('temperature')
    iid = request.json.get('id')
    if vtemperature is None or iid is None:
        abort(400)
    else:
        temperatureOBJ = Temperature(iid, vtemperature)
        db.session.add(temperatureOBJ)
        db.session.commit()

    return jsonify({'id' : iid, 'temperatura' : vtemperature})

@app.route('/RFIDCadastraConsulta', methods=['POST'])
def RFIDCadastraConsulta():
    IdRFID = request.json.get('IDRFID')
    iid = request.json.get('id')
    if IdRFID is None or iid is None:
        abort(400)
    return jsonify({'id' : iid, 'RFID' : IdRFID})

@app.route('/dashboard')
def dashboard():
	if 'email' not in session:
		return redirect(url_for('signin'))

	user = User.query.filter_by(email = session['email']).first()

	if user is None:
		return redirect(url_for('signin'))
	else:
		return render_template('dashboard.html')\

@app.errorhandler(404)
def page_not_found(e):
	return render_template('page-404.html'), 404

@app.route('/createPerson', methods=['GET', 'POST'])
def createPerson():
	if 'email' not in session:
		return redirect(url_for('signin'))

	form = CreatePersonForm()
	user = User.query.filter_by(email = session['email']).first()
	currentProfile = Profile.query.filter_by(uid = user.uid).first()

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('createPerson.html', form=form)
		else:
			profileEmployee = Profile(user.uid, form.firstname.data, form.lastname.data, form.cpf.data, form.birthDate.data, form.rg.data, form.address.data, int(form.number.data), form.additionalInformation.data, form.district.data, form.region.data, form.country.data, form.telephone.data, form.cellphone.data, 'E', form.role.data, form.bloodType.data)
			db.session.add(profileEmployee)
			db.session.commit()
			return redirect(url_for('createPerson'))

	elif request.method == "GET":
		if user is None:
			return redirect(url_for('signin'))
		else:
			if currentProfile.role == 'Administrador(a)':
				return render_template('createPerson.html', form=form)
			else:
				return redirect('403_page')

@app.route('/403_page')
def permissionDeniedPage():
	return render_template('page-403.html')

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