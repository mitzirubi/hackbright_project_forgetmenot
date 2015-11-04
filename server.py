""" Forgetmenot Instagram likes"""


from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import Place, User, LikedImage, Category, connect_to_db, db

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

################################################################################


@app.route('/welcome')
def welcome_page():
    """Homepage."""

    return render_template("welcome.html")


@app.route('/authentication')
def user_authentication():
    """This will prompt the user to authorize Forgetmenot to their IG account."""
    pass


#this will be in optional user profile data!
# @app.route('/register', methods=['GET'])
# def register_form():
#     """Show form for user signup."""

#     return render_template("registration_form.html")


# @app.route('/register', methods=['POST'])
# def register_process():
#     """New user login information."""

#     # Get form variables from form in POST request
#     email = request.form['email']
#     password = request.form['password']
#     username = request.form['username']

#     new_registered_user = User.query.filter_by(username=User.username).first()

#     if not new_registered_user:
#         flash("You first need to connect Forgetmenot to Instagram")
#         return redirect("/welcome")
#         #my OAuth will be in the welcome page!

#     if new_registered_user.username == User.username:
#         new_registered_user.password = password
#         new_registered_user.email = email

#         db.session.commit()

#         session["user_id"] = user.user_id

#         flash("Your username %s has been verified, %s and %s have been added to your profile.") % (username, email, password)
#         return redirect('/myprofile')


#Once user have authenticated and registerd their information then they can login
#UPDATE Users SET user_email="email",user_password ="pw" Where user_id='id';
#Added my information to debug route


@app.route('/login_confirmation', methods=['POST'])
def login_process():
    """Process login request"""

    # Get form variables via POST request
    username = request.form['username']

    password = request.form["password"]

    user = User.query.filter_by(username=username).first()

    print user

    if not user:
        flash("User is not registered, please login with Instagram")
        return redirect("/welcome")

    if user.user_password != password:
        flash("Incorrect username or password. Please try again!")
        return redirect("/welcome")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect('/forgetmenotfavorites')


@app.route('/forgetmenotfavorites')
def forgetmenotfavorites():
    """Render all of the users favorited IG posts this is the main page."""

    user_id = session["user_id"]

    likedimages = LikedImage.query.filter_by(user_id=user_id).all()  # User id in the session right now ). pass the user to jinja
                                                       #template = python
    return render_template('forgetmenotfavorites.html', likedimages=likedimages)


@app.route('/myprofile')
def show_user_profile():
    """Render the user profile and show their basic info and visited likes."""

    return render_template('userprofile.html')


@app.route('/favoritedinfo')
def favoritedinfo():
    """Shows a photo profile info, in our case all of the restaurant profile"""
    pass

@app.route('/mapmehere')
def findmehere():
    """Displays all of users favorited IG posts in a map view"""
    pass


# @app.route('/logout')
#     """Displays all of users favorited IG posts in a map view"""
#     pass


################################################################################


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True
    app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
