"""Models and database functions for Forgetmenot project."""

from flask_sqlalchemy import SQLAlchemy
import datetime

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class Restaurants(db.Model):
    """Restaurants users have liked on IG Account stored in forgetmenot"""

    __tablename__ = "restaurants"

    restaurant_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
    restaurant_name = db.Column(db.String(200), nullable=True)  #because some photos may not have locations
    image_url = db.Column(db.String(200), nullable=False)
    thumbnail_url = db.Column(db.String(200), nullable=False)
    user_notes = db.Column(db.Text, nullable=True)  ##.Text
    liked_at = db.Column(db.DateTime, nullable=False)  #is this the correct timestamp adder? yes
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    visited_at = db.Column(db.Boolean, default=False, nullable=False)   #the date you visitied the location true or false instead
    category_id = db.Column(db.Integer, db.ForeignKey('Categories.category_id'))

    def __repr__(self):
        """Provide helpful information about the restaurant."""

        return ("<Restaurant restaurant_id=%s user_id=%s \
                restaurant_name=%s>") % (self.restaurant_id,
                                          self.user_id, self.restaurant_name)
class  Locations(db.Model):
    """Location information of restaurant will help with relationship"""
    location_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    latitude = db.Column(db.Integer, nullable=True)   #location of restaurant
    longitude = db.Column(db.Integer, nullable=True)   #location of restuarant
    category_id = db.Column(db.Integer, db.ForeignKey('Categories.category_id'))
    Street1 = db.Column(db.Integer(150), nullable=True)
    apt = db.Column(db.String(10), nullable=True)
    city = db.Column(db.String(50),nullable=True)
    state = db.Column(db.String(50), nullable=True)
    zip_code =db.Column(db.Integer(30), nullable=True)
    country =db.Column(db.Integer(20), nullable=True)

class RestaurantLocation(db.Model):
    """relationship between restaurants and locations"""

    __tablename__ = "RestaurantLocation"

    restaurant_id =db.Column(db.Integer,db.ForeignKey('restaurants.restaurant_id'))
    location_id = db.Column(db.Integer,db.ForeignKey('locations.location_id'))

    #define relationsip of restaurants to location
    restlocation_id = (db.relationship("Location", backref=db.backref(RestaurantLocation),
                                                  order_by=restaurant_id,primary_key=True))

    def __repr__(self):
        """provide helpful information about relationship of restuarant and locations"""

        return "<RestaurantLocation rest_location_id=%s restaurant_id location_id=%s>" % (self.restlocation_id,
                                                                                   self.restaurant_id,
                                                                                   self.location_id)

class Users(db.Model):
    """User information from IG accounts."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    user_email = db.Column(db.String(100), nullable=True)
    profile_picture = db.Column(db.String(200), nullable=True)
    access_token = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        """Provide helpful information about the user"""

        return ("<User user_id=%s username=%s access_token=%s>") % (self.user_id,
                                                                   self.username,
                                                                   self.access_token)

class UserRestaurantslikes (object):
    """User relationship to Restaurants of IG posts they have liked."""

    __tablename__ = "UserRestaurantslikes"

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.restaurant_id'))
    user_notes = db.Column(db.Text, db.ForeignKey('restaurants.user_notes'))

    ##define relationsip of user to restaurants
    user= db.relationship("Restaurants",backref=db.backref("UserRestaurantslikes", order_by=created_at,primary_key=True))
    #do i need a relationship of restaurants ex: reaturant = db.relationship("Users", backbref=db.backfres("UserRestaurantslikes"), order_by=created_at, )

    def __repr__(self):
        """provide helpful information about restuarant and user information"""

        return "<UserRestaurantslikes user_id =%s restaurant_id user_notes=%s>" % (self.user_id,
                                                                                   self.restaurant_id,
                                                                                   self.user_notes)
class Categories(db.Model):
    """Catergorize IG Photos"""

    __tablename__ = "categories"

    category_id = db.Column(db.Interger, autoincrement=True, primary_key=True)

    def __repr__(self):
        """Provide helpful information about the image category"""

        return ("<Category category_id=%s>") % (self.category_id)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database (app is an instance and config is a dictionary)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forgetmenot.db'   #created a new db link
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
