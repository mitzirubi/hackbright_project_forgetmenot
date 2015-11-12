""" Forgetmenot Instagram likes"""


from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify
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
#         return redirect('/placesvisited')


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

@app.route('/logout', methods=['POST'])
def logout():
    """Log out."""

    del session["user_id"]
    flash("Thanks for stopping by, we hope to see you again!")
    return redirect("/welcome")


@app.route('/forgetmenotfavorites')
def forgetmenotfavorites():
    """Render all of the users favorited IG posts this is the main page."""

    user_id = session["user_id"]

    # User id in the session right now ). pass the user to jinja
    likedimages = LikedImage.query.filter_by(user_id=user_id).all()


                                                         #template = python
    return render_template('forgetmenotfavorites.html', likedimages=likedimages)


@app.route('/placesvisited', methods=['GET', 'POST'])
def show_user_profile():
    """Render the user profile and show their basic info and visited likes."""

    # visited = request.form.getlist('visited')
    image_id_list = request.form.getlist('visited')
    print image_id_list

    for image_id in image_id_list:

        user_liked_image = LikedImage.query.filter(LikedImage.liked_image_id == image_id, LikedImage.user_id == 1).first()
        print user_liked_image

        user_liked_image.visited = True

        # test = user_liked_image.visited
        # print test
    db.session.commit()

    user = User.query.filter_by(user_id=session['user_id']).first()

    username = user.username
    profile_picture = user.profile_picture

    visited = LikedImage.query.filter_by(user_id=session['user_id'], visited=True).count()

    return render_template('placesvisited.html', image_id_list=image_id_list, username=username,
                           profile_picture=profile_picture, user=user, visited=visited)


@app.route("/likedimageinfo/<int:place_id>", methods=['GET'])
def likedimageinfo(place_id):
    """Shows a photo profile info, in our case all of the restaurant profile"""

    likedimage = LikedImage.query.filter_by(place_id=place_id, user_id=session['user_id']).first()
    print likedimage


    place_id  = likedimage.place.place_id
    print place_id
    place_name = likedimage.place.place_name
    latitude = likedimage.place.latitude
    longitude = likedimage.place.longitude
    user_note = likedimage.user_note
    visited = likedimage.visited


    return render_template("likedimageinfo.html", place_id=place_id, place_name=place_name,
                           latitude=latitude, longitude=longitude, place_info=likedimage.place, visited=visited,
                           user_note=user_note)

@app.route('/usernotes.json', methods=["POST"])
def update_user_notes():
    # save the new user notes in DB
    print "*** GOT HERE"
    user_note = request.form.get('user_notes')
    place_id = request.form.get('placeId')

    print '\n\n\n\n', user_note, place_id, '\n\n\n\n'


    user_id = session.get("user_id")

    print '\n\n\n\n', user_id, '\n\n\n\n'

    if not user_id:
        flash("User not logged in.")
        return redirect("/welcome")

    else:                                           #model=server route
        print place_id
        get_likedImage = LikedImage.query.filter_by(user_id=user_id,place_id=place_id).first()
        print get_likedImage ##incorrect place id is shown here and committed
        print place_id
        get_likedImage.user_note = user_note
        print get_likedImage

        db.session.commit()

    return jsonify({'save': 'successful'})


@app.route('/display_user_notes/<int:place_id>.json')
def getusernotes(place_id):

    notes = LikedImage.query.filter_by(user_id=session['user_id'], place_id=place_id).first()
    print notes
    user_note = {'user_id': session['user_id'], 'place_id': place_id, 'user_note': notes.user_note}
    print user_note
    display_notes = jsonify(user_note)
    return display_notes


@app.route('/mapmehere')
def findmehere():
    """Displays all of users favorited IG posts in a map view"""

    return render_template('mapmehere.html')

@app.route('/photo_info.json')
def photo_info():
    """JSON information about photo and place details."""

    list_of_liked_objects = db.session.query(LikedImage, Place).filter_by(user_id=session['user_id']).join(Place).all()

    list_of_places = []

    for image, place in list_of_liked_objects:
                        #key/value
        place_info = {
                "placeId": place.place_id,
                "placeName": place.place_name,
                "category": place.category,
                "latitude": place.latitude,
                "longitude": place.longitude,
                "igPlaceId": place.instagram_place_id,
                "imageUrl": image.image_url,
                "visited": image.visited
            }

        list_of_places.append(place_info)

    places_dict = {'places': list_of_places}

    return jsonify(places_dict)


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
