from flask import Flask, render_template, request, redirect
from .models import *
import bcrypt
from .base import Session
from sqlalchemy import update
from imgurpython import ImgurClient
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config.from_object('config')

Base.metadata.create_all(engine)
session = Session()

client = ImgurClient(app.config['IMGUR_ID'], app.config['IMGUR_PK'])
UPLOAD_FOLDER = '\\annuaire\\static\\img\\'

auth = 0

@app.route('/')
def index():
    return render_template('index.html', auth=auth)


@app.route('/inscription/', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        hashed = bcrypt.hashpw(request.form.get('password').encode(), bcrypt.gensalt())
        db.session.add(User(firstname=request.form.get('firstname'), lastname=request.form.get('lastname'), email=request.form.get('email'), password=hashed))
        db.session.commit()

    return render_template('inscription.html',auth=auth)


@app.route('/connexion/', methods=['GET', 'POST'])
def connexion():
    global auth
    if auth == 1:
        return redirect("../dashboard/")

    if request.method == 'POST':
        user = session.query(User).filter(User.email == request.form.get('email')).first()

        if user is None:
            return render_template('connexion.html',auth=auth)
        
        hashed = user.password
        
        if bcrypt.checkpw(request.form.get('password').encode(), hashed.encode()):
            auth = user.id
            return redirect("../dashboard/")

    return render_template('connexion.html',auth=auth)


@app.route('/logout/')
def logout():
    global auth
    auth = 0
    return redirect("../")


@app.route('/dashboard/', methods=['GET', 'POST'])
def dashboard():
    global auth
    if auth == 0:
        return redirect("../connexion/")

    users = session.query(User).all()
    return render_template('app.html', auth=auth, users = users)


@app.route('/search')
def search():
    global auth
    if auth == 0:
        return redirect("../connexion/")

    users1 = session.query(User).filter(User.email == request.form.get('email')).all()
    users2 = session.query(User).filter(User.firstname == request.args.get('firstname')).all()
    users3 = session.query(User).filter(User.lastname == request.args.get('lastname')).all()
    users4 = session.query(User).filter(User.phone == request.args.get('phone')).all()

    users = users1 + users2 + users3 + users4
    users = list(dict.fromkeys(users))
    
    return render_template('app.html', auth=auth, users = users, email = request.args.get('email'), firstname = request.args.get('firstname'), lastname = request.args.get('lastname'), phone = request.args.get('phone') )


@app.route('/profile/', methods=['GET', 'POST'])
def profile():
    global auth
    if auth == 0:
        return redirect("../connexion/")

    user = session.query(User).filter(User.id == auth).first()
    
    print(type(user))
    print("[DEBUG] before : ", user.firstname)

    if request.method == "POST":
        session.flush()
        conn = engine.connect()

        file = request.files['picture']
        if file:
            filename = secure_filename(file.filename)
            path = os.getcwd() + UPLOAD_FOLDER + filename
            file.save(path)
            image = client.upload_from_path(path)
            picture = image['link']

            stmt = (
                update(User).
                where(User.id == auth).
                values(firstname=request.form.get('firstname'), lastname=request.form.get('lastname'), email=request.form.get('email'), phone=request.form.get('phone'), description=request.form.get('description'), picture=picture)
            )
        else:
            stmt = (
                update(User).
                where(User.id == auth).
                values(firstname=request.form.get('firstname'), lastname=request.form.get('lastname'), email=request.form.get('email'), phone=request.form.get('phone'), description=request.form.get('description'))
            )

        conn.execute(stmt)
        session.commit()
        print("[DEBUG]  ", stmt)

    user = session.query(User).filter(User.id == auth).first()
    return render_template('profile.html', auth=auth, user=user)


if __name__ == "__main__":
    app.run()