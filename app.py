"""Flask App for Flask Cafe."""

from flask import Flask, render_template, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
import os
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, Cafe, City, User
from forms import AddEditCafeForm, SignupForm, LoginForm


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flaskcafe'
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "shhhh")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

toolbar = DebugToolbarExtension(app)

connect_db(app)

#######################################
# auth & auth routes

CURR_USER_KEY = "curr_user"
NOT_LOGGED_IN_MSG = "You are not logged in."


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


#######################################
# homepage

@app.get("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")

#######################################
# user authorization

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to database. Redirect to cafe list.

    If form not valid, present form.

    Check if username is taken and if so, flash relevant message
    """

    do_logout()

    form = SignupForm()

    if form.validate_on_submit():
        user = User.register(
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            description=form.description.data,
            password=form.password.data,
            email=form.email.data,
            image_url=form.image_url.data or None,
        )

        try:
            db.session.commit()

        except IntegrityError:
            flash("Username taken, pick a new username", 'danger')
            return render_template('auth/signup-form.html', form=form)

        do_login(user)

        flash("Sign up successful!")
        return redirect("/cafes")

    else:
        return render_template('auth/signup-form.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login. Redirects to cafe list if successful."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f"{user.username} logged in", 'success')
            return redirect("/cafes")

        flash("Incorrect username or password", 'danger')

    return render_template('auth/login-form.html', form=form)

@app.post('/logout')
def logout():
    """Handle user logout. Redirects to homepage."""

    do_logout()

    flash("Log out successful", 'success')
    return redirect("/")


#######################################
# cafes


@app.get('/cafes')
def cafe_list():
    """Return list of all cafes."""

    cafes = Cafe.query.order_by('name').all()

    return render_template(
        'cafe/list.html',
        cafes=cafes,
    )


@app.get('/cafes/<int:cafe_id>')
def cafe_detail(cafe_id):
    """Show detail for cafe."""

    cafe = Cafe.query.get_or_404(cafe_id)

    return render_template(
        'cafe/detail.html',
        cafe=cafe,
    )

@app.route('/cafes/add', methods=['GET', 'POST'])
def add_cafe():
    '''Add a cafe or show form to add a cafe'''

    form = AddEditCafeForm()
    form.city_code.choices = City.get_choices_vocab()

    if form.validate_on_submit():
        cafe = Cafe(
            name=form.name.data,
            description=form.description.data,
            url=form.url.data,
            address=form.address.data,
            city_code=form.city_code.data,
            image_url=form.image_url.data or None,
        )

        db.session.add(cafe)
        db.session.commit()

        flash(f'{cafe.name} added')
        return redirect(f'/cafes/{cafe.id}')

    return render_template('cafe/add-form.html', form=form)

@app.route('/cafes/<int:cafe_id>/edit', methods=['GET', 'POST'])
def edit_cafe(cafe_id):
    '''Edit a cafe or show form to edit a cafe'''

    cafe = Cafe.query.get_or_404(cafe_id)

    form = AddEditCafeForm(obj=cafe)
    form.city_code.choices = City.get_choices_vocab()

    if form.validate_on_submit():
        cafe = Cafe(
            name=form.name.data,
            description=form.description.data,
            url=form.url.data,
            address=form.address.data,
            city_code=form.city_code.data,
            image_url=form.image_url.data or None,
        )

        db.session.add(cafe)
        db.session.commit()

        flash(f'{cafe.name} edited')
        return redirect(f'/cafes/{cafe.id}')

    return render_template('cafe/edit-form.html', form=form, cafe=cafe)
