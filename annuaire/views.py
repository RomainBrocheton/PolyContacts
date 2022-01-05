from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from .models import *
import bcrypt

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
auth = 0

@app.route('/')
def index():
    return render_template('index.html', auth=auth)

@app.route('/inscription/', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        hashed = bcrypt.hashpw(request.form.get('password').encode(), bcrypt.gensalt())
        db.session.add(User(request.form.get('firstname'), request.form.get('lastname'), request.form.get('email'), hashed))
        db.session.commit()

    return render_template('inscription.html',auth=auth)

@app.route('/connexion/', methods=['GET', 'POST'])
def connexion():
    global auth
    if auth == 1:
        return redirect("../dashboard/")

    if request.method == 'POST':
        user = User.query.filter(User.email == request.form.get('email')).first()

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

    return render_template('app.html',auth=auth)

if __name__ == "__main__":
    app.run()