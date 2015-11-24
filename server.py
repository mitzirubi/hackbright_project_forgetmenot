""" Forgetmenot Instagram likes"""


from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify, abort
from flask_debugtoolbar import DebugToolbarExtension

from model import Place, User, LikedImage, Category, connect_to_db, db
import model
import requests
import pprint
import os

# from instagram.client import InstagramAPI
# import time

# printer = pprint.PrettyPrinter()
# access_token = os.environ['ACCESS_TOKEN']
geocode_key = os.environ['GEOCODE_KEY']

# instaConfig = {
#     'client_id':os.environ.get('CLIENT_ID'),
#     'client_secret':os.environ.get('CLIENT_SECRET'),
#     'redirect_uri' : os.environ.get('REDIRECT_URI')
# }
# api = InstagramAPI(**instaConfig)

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

    flash("Welcome %s , you are now logged in." % username)
    return redirect('/forgetmenotfavorites')

@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Thanks for stopping by, we hope to see you again!")
    return redirect("/welcome")


@app.route('/forgetmenotfavorites')
def forgetmenotfavorites():
    """Render all of the users favorited IG photos, this is the main page."""

    user_id = session["user_id"]

    # User id in the session right now pass the user to jinja
    likedimages = LikedImage.query.filter_by(user_id=user_id).all()


                                                         #template = python
    return render_template('forgetmenotfavorites.html', likedimages=likedimages)


@app.route('/placesvisited', methods=['GET', 'POST'])
def show_user_profile():
    """Render the user profile and show their basic info and visited likes."""

    # print request.form
    for place_id in request.form.keys():
        for value in request.form.getlist(place_id):

            print place_id, ":", value

        user_liked_image = LikedImage.query.filter(LikedImage.place_id == place_id,
                           LikedImage.user_id == session['user_id']).all()

        if request.form.get(place_id) == "no":
            for liked_image in user_liked_image:
                liked_image.visited = False
        else:
            for liked_image in user_liked_image:
                liked_image.visited = True

    db.session.commit()

    user = User.query.filter_by(user_id=session['user_id']).first()

    username = user.username
    profile_picture = user.profile_picture

    visited = LikedImage.query.filter_by(user_id=session['user_id'], visited=True).count()

    liked_visited_images = LikedImage.query.filter_by(user_id=session['user_id'], visited=True).all()

    # make a unique list of each place that the user has visited
    user_places = set()
    for liked_image in liked_visited_images:
        user_places.add(liked_image.place)


    return render_template('placesvisited.html',
                            username=username,
                            profile_picture=profile_picture,
                            user=user,
                            visited=visited,
                            user_places=user_places)


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
    address = likedimage.place.address


    return render_template("likedimageinfo.html",
                           place_id=place_id,
                           place_name=place_name,
                           latitude=latitude,
                           longitude=longitude,
                           address=address,
                           place_info=likedimage.place,
                           visited=visited,
                           user_note=user_note)

@app.route('/usernotes.json', methods=["POST"])
def update_user_notes():
    # save the new user notes in DB
    # print "*** GOT HERE***"
    user_note = request.form.get('user_notes')
    place_id = request.form.get('placeId')

    # print user_note, place_id

    user_id = session.get("user_id")

    # print user_id

    if not user_id:
        flash("User not logged in.")
        return redirect("/welcome")

    else:                                           #model=server route
        get_likedImage = LikedImage.query.filter_by(user_id=user_id,place_id=place_id).first()
        print get_likedImage  
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

@app.route('/map_photo_info.json')
def photo_info():
    """JSON information about photo and place details."""

    list_of_liked_objects = db.session.query(LikedImage, Place).filter_by(user_id=session['user_id']).join(Place).all()
    print list_of_liked_objects

    list_of_places = []

    for image, place in list_of_liked_objects:
        if image.visited is True:
            image.visited = "Yes"
        else:
            image.visited = "Not visited"
        if not image.user_note:
            image.user_note = "Sorry, you have no notes."


        print image
                        #key/value
        place_info = {
                "placeId": place.place_id,
                "placeName": place.place_name,
                "category": place.category,
                "latitude": place.latitude,
                "longitude": place.longitude,
                "address" : place.address,
                "igPlaceId": place.instagram_place_id,
                "imageUrl": image.image_url,
                "visited": image.visited,
                "user_note": image.user_note
            }

        list_of_places.append(place_info)

    places_dict = {'places': list_of_places}
    print places_dict

    return jsonify(places_dict)


################################################################################


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True
    app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    # app.run()

    port = int(os.environ.get('PORT', 5000)) # locally PORT 5000, Heroku will assign its own port
    app.run(host='0.0.0.0', port=port)
