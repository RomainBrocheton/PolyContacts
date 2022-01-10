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

    users = User.query.all()
    return render_template('app.html', auth=auth, users = users)


@app.route('/search')
def search():
    global auth
    if auth == 0:
        return redirect("../connexion/")

    users1 = User.query.filter(User.email == request.args.get('email')).all()
    users2 = User.query.filter(User.firstname == request.args.get('firstname')).all()
    users3 = User.query.filter(User.lastname == request.args.get('lastname')).all()
    users4 = User.query.filter(User.phone == request.args.get('phone')).all()

    users = users1 + users2 + users3 + users4
    users = list(dict.fromkeys(users))
    return render_template('app.html', auth=auth, users = users, email = request.args.get('email'), firstname = request.args.get('firstname'), lastname = request.args.get('lastname'), phone = request.args.get('phone') )


@app.route('/profile/', methods=['GET', 'POST'])
def profile():
    global auth
    if auth == 0:
        return redirect("../connexion/")

    db.session.flush()
    user = User.query.get(auth)
    print(type(user))
    print("[DEBUG] before : ", user.firstname)

    if request.method == "POST":    # BUG update not working
        user.firstname = "test"
       #user.firstname = request.form.get("firstname")
        user.lastname = request.form.get("lastname")
        user.email = request.form.get("email")
        user.phone = request.form.get("phone")
        user.description = request.form.get("description")

        print(db.session.dirty)
        print(db.session.commit())
        print(db.session.dirty)

        print("[DEBUG] after : ", user.firstname)

    user = User.query.get(auth)
    return render_template('profile.html', auth=auth, user=user)


if __name__ == "__main__":
    app.run()