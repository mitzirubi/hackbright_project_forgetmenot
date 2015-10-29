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

@app.route('/forgetmenot')  # homepage.html
def homepage():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/authentication')
def user_authentication():
    """This will prompt the user to authorize Forgetmenot to their IG account."""
    if user:
        session['']

@app.route('/forgetmenotfavorites')
def forgetmenotfavorties():
    """Render all of the users favorited IG posts."""
    pass

@app.route('/myprofile')
def myprofile():
    """Render the user profile and show their basic info and visited likes."""
    pass

@app.route('/favoritedinfo')
def favoritedinfo():
    """Shows a photo profile info, in our case all of the restaurant profile"""
    pass

@app.route('/mapmehere')
def findmehere():
    """Displays all of users favorited IG posts in a map view"""
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
