from UTIntensa import app
from flask import render_template, request, flash, session, url_for, redirect, jsonify
from forms import ContactForm, SigninForm, ProfileForm, CreatePersonForm, CreateMedicalAppointment, CreateMedicamentType, CreateMedicament
from flask.ext.mail import Message, Mail
from models import db, User, Profile, Temperature, Heartbeat, event, dashboard, medicamentType, medicament, records, room
import json

mail = Mail()
idDash = 0;

@app.route('/testdb')
def testdb():
    if db.session.query("1").from_statement("SELECT 1").all():
        return 'It works.'
    else:
        return 'Something is broken.'

@app.route('/')
def home():
    return redirect(url_for('profile'))
  
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
    IdRFID = request.json.get('idrfid')
    iid = request.json.get('id')
    idRoom = request.json.get('idroom')
    if IdRFID is None or iid is None:
        abort(400)

    cuser = User.query.filter_by(rfid = IdRFID).first()

    temp = Temperature.query.filter(Temperature.idPatient == iid, Temperature.vitalSign == "Temperature").order_by(Temperature.dateConsulting.desc()).first()
    heart = Heartbeat.query.filter(Heartbeat.idPatient == iid, Heartbeat.vitalSign == "Heartbeat").order_by(Heartbeat.dateConsulting.desc()).first()
    eventOBJ = event("", idRoom, temp.value, heart.value, iid, cuser.uid)
    db.session.add(eventOBJ)
    db.session.commit()

    return jsonify({'id' : iid})

@app.route('/dashboard', methods=['GET','POST'])
def dashboardMethod():
    if 'email' not in session:
      return redirect(url_for('signin'))

    user = User.query.filter_by(email = session['email']).first()
    profile = Profile.query.filter_by(uid = user.uid).first()
    dashboardlist = []

    count = Profile.query.filter_by(role = "Paciente").count()
    patients = Profile.query.filter(Profile.role == "Paciente").all()
    index = 0
    for p in patients:
        temp = Temperature.query.filter(Temperature.idPatient == p.uid, Temperature.vitalSign == "Temperature").order_by(Temperature.dateConsulting.desc()).first()
        heart = Heartbeat.query.filter(Heartbeat.idPatient == p.uid, Heartbeat.vitalSign == "Heartbeat").order_by(Heartbeat.dateConsulting.desc()).first()
        p = dashboard(p.firstname, p.lastname, heart.value, temp.value, p.birthdate, p.uid)
        dashboardlist.append(p)
        index = index + 1

    updateobj = dashboardlist
    objectUpdate = json.dumps({'data': [o.serialize for o in updateobj]})

    if user is None:
        return redirect(url_for('signin'))
    else:
        print "chamou dashboard.html"
        return render_template('dashboard.html', data=dashboardlist, objectUpdate=objectUpdate)

@app.route('/dashboardUpdate', methods=['GET','POST'])
def dashboardUpdate():
    user = User.query.filter_by(email = session['email']).first()
    dashboardlist = []

    patients = Profile.query.filter(Profile.role == "Paciente").all()

    for p in patients:
        temp = Temperature.query.filter(Temperature.idPatient == p.uid, Temperature.vitalSign == "Temperature").order_by(Temperature.dateConsulting.desc()).first()
        heart = Heartbeat.query.filter(Heartbeat.idPatient == p.uid, Heartbeat.vitalSign == "Heartbeat").order_by(Heartbeat.dateConsulting.desc()).first()
        p = dashboard(p.firstname, p.lastname, heart.value, temp.value, p.birthdate, p.uid)
        dashboardlist.append(p)

    updateobj = dashboardlist
    objectUpdate = json.dumps({'data': [o.serialize for o in updateobj]})
    return objectUpdate

@app.errorhandler(404)
def page_not_found(e):
    return render_template('page-404.html')

@app.route('/CreateMedicamentType', methods=['GET', 'POST'])
def createMedicamentType():
    if 'email' not in session:
        return redirect(url_for('signin'))

    form = CreateMedicamentType()
    user = User.query.filter_by(email = session['email']).first()
    currentProfile = Profile.query.filter_by(uid = user.uid).first()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('CreateMedicamentType.html', form=form)
        else:
            mType = medicamentType(form.name.data, form.description.data, form.labelm.data)
            db.session.add(mType)
            db.session.commit()
            return redirect(url_for('createMedicamentType'))

    elif request.method == "GET":
        if user is None:
            return redirect(url_for('signin'))
        else:
            if currentProfile.role == 'Administrador(a)':
                return render_template('CreateMedicamentType.html', form=form)
            else:
                return redirect('403_page')

@app.route('/CreateMedicament', methods=['GET', 'POST'])
def createMedicament():
    if 'email' not in session:
        return redirect(url_for('signin'))

    form = CreateMedicament()
    user = User.query.filter_by(email = session['email']).first()
    currentProfile = Profile.query.filter_by(uid = user.uid).first()

    if request.method == 'POST':
        med = medicament(form.description.data, form.type.data)
        print med.description
        print med.type
        db.session.add(med)
        db.session.commit()
        return redirect(url_for('createMedicament'))

    elif request.method == "GET":
        if user is None:
            return redirect(url_for('signin'))
        else:
            if currentProfile.role == 'Administrador(a)':
                return render_template('CreateMedicament.html', form=form)
            else:
                return redirect('403_page')

@app.route('/RecordsList')
def recordsList():
    if 'email' not in session:
        return redirect(url_for('signin'))

    return render_template('Records.html')

@app.route('/CreateRecords', methods=['GET', 'POST'])
def createRecords():
    if 'email' not in session:
        return redirect(url_for('signin'))

    form = CreateMedicalAppointment()
    user = User.query.filter_by(email = session['email']).first()
    profile = Profile.query.filter_by(uid = user.uid).first()
    form.updateHeaderData(profile)

    if request.method == 'POST':
        ev = event("", form.idRoom.data, form.temp.data, form.heart.data, user.uid, form.idPatient.data)
        db.session.add(ev)
        db.session.commit()
        record = records(form.idRoom.data, user.uid, form.idPatient.data, form.idMedicament.data, form.description.data, form.dose.data, form.unitMeasure.data, ev.id)
        db.session.add(record)
        db.session.commit()

        return redirect(url_for('createRecords'))

    elif request.method == "GET":
        if user is None:
            return redirect(url_for('signin'))
        else:
            return render_template('createRecords.html', form=form)

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
            if form.role.data == "Paciente":
                profileEmployee = Profile(user.uid, form.firstname.data, form.lastname.data, form.cpf.data, form.birthDate.data, form.rg.data, form.address.data, int(form.number.data), form.additionalInformation.data, form.district.data, form.region.data, form.country.data, form.telephone.data, form.cellphone.data, 'P', form.role.data, form.bloodType.data)
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

@app.route('/dashboard-detail/<int:id>')
def dashboardDetail(id):
    if 'email' not in session:
        return redirect(url_for('signin'))

    patient = Profile.query.filter_by(uid = id).first()
    temp = Temperature.query.filter(Temperature.idPatient == patient.uid, Temperature.vitalSign == "Temperature").order_by(Temperature.dateConsulting.desc()).first()
    heart = Heartbeat.query.filter(Heartbeat.idPatient == patient.uid, Heartbeat.vitalSign == "Heartbeat").order_by(Heartbeat.dateConsulting.desc()).first()
    e = event.query.filter_by(idPatient = id).order_by(event.date.desc(), event.time.desc()).first()
    r = room.query.filter_by(id = e.idRoom).first()
    dash = dashboard(patient.firstname, patient.lastname, heart.value, temp.value, patient.birthdate, patient.uid);

    return render_template('dashboard-detail.html', patient=patient, dash=dash, room=r)

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

@app.route('/calendario/<int:id>')
def calendario(id):
    if 'email' not in session:
        return redirect(url_for('signin'))

    e = event.query.filter_by(idPatient = id).all()
    eventslist = []
    for ev in e:
        eventslist.append(ev)

    updateobj = eventslist
    objectUpdate = json.dumps({'data': [o.serialize for o in updateobj]})


    return render_template('calendario.html', ev=objectUpdate)

@app.route('/signout')
def signout():
  
    if 'email' not in session:
        return redirect(url_for('signin'))
     
    session.pop('email', None)
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True, threaded=True)