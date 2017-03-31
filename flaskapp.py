from flask import Flask, render_template, request, session, redirect, url_for
from models import db, User, Place, Event
from forms import SignupForm, LoginForm, AddressForm, EventsForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kidstime:Sairam18@kidstime.ckxjvp0zvc4h.us-west-2.rds.amazonaws.com/kidstimedb'
db.init_app(app)

app.secret_key = "development-key"

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
  if 'email' in session:
    return redirect(url_for('places'))

  form = SignupForm()

  if request.method == "POST":
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()

      session['email'] = newuser.email
      return redirect(url_for('places'))

  elif request.method == "GET":
    return render_template('signup.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
  if 'email' in session:
    return redirect(url_for('places'))

  form = LoginForm()

  if request.method == "POST":
    if form.validate() == False:
      return render_template("login.html", form=form)
    else:
      email = form.email.data
      password = form.password.data

      user = User.query.filter_by(email=email).first()
      if user is not None and user.check_password(password):
        session['email'] = form.email.data
        return redirect(url_for('places'))
      else:
        return redirect(url_for('login'))

  elif request.method == 'GET':
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
  session.pop('email', None)
  return redirect(url_for('index'))

@app.route("/places", methods=["GET", "POST"])
def places():
  if 'email' not in session:
    return redirect(url_for('login'))

  form = AddressForm()

  places = []
  my_coordinates = (37.4221, -122.0844)

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('places.html', form=form)
    else:
      # get the address
      address = form.address.data

      # query for places around it
      p = Place()
      my_coordinates = p.address_to_latlng(address)
      places = p.query(address)

      # return those results
      return render_template('places.html', form=form, my_coordinates=my_coordinates, places=places)

  elif request.method == 'GET':
    return render_template("places.html", form=form, my_coordinates=my_coordinates, places=places)
@app.route("/events", methods=["GET", "POST"])
def events():
  if 'email' not in session:
    return redirect(url_for('login'))

  form = AddressForm()

  events_list = []
  my_coordinates = (37.4221, -122.0844)

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('events.html', form=form)
    else:
      # get the address
      address = form.address.data

      # query for places around it
      e = Event()
      my_coordinates = e.address_to_latlng(address)
      events_list = e.query(address)

      # return those results
      return render_template('events.html', form=form, my_coordinates=my_coordinates, events=events_list)

  elif request.method == 'GET':
    return render_template("events.html", form=form, my_coordinates=my_coordinates, events=events_list)

if __name__ == "__main__":
  app.run(debug=True)
