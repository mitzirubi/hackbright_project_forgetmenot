""" Forgetmenot Instagram likes"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import Restaurant, Location, RestaurantLocation,User, UserRestaurantslike, Category, connect_to_db, db

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined
################################################################################

@app.route('/forgetmenot')
def homepage():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/authentication')
def user_authentication():
    pass

@app.route('/remembermelikes')
def rememberme():
    pass

@app.route('/myprofile')
def myprofile():
    pass

@app.route('/likesinfo')
def likesinfo():
    pass

@app.route('/mapmehere')
def findmehere():
    pass

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
