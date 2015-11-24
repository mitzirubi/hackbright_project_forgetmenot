"""Models and database functions for Forgetmenot project."""

from flask_sqlalchemy import SQLAlchemy
import datetime

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User information from IG accounts."""

    __tablename__ = "Users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(75), nullable=False)
    user_email = db.Column(db.String(100), nullable=True)
    profile_picture = db.Column(db.String(200), nullable=True)
    access_token = db.Column(db.String(80), nullable=True)
    client_id = db.Column(db.String(80), nullable=True)  # added this because of OAuth making nullable true, can change after project season
    user_password = db.Column(db.String(40), nullable=True)

    def __repr__(self):
        """Provide helpful information about the user"""

        return ("<User user_id=%s username=%s access_token=%s>") % (self.user_id,
                                                                    self.username,
                                                                    self.access_token)


class Place(db.Model):
    """Places users have liked on IG Account stored in forgetmenot"""

    __tablename__ = "Places"

    place_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    place_name = db.Column(db.String(200), nullable=True)  # some photos may not have locations
    category = db.Column(db.String(50), db.ForeignKey('Categories.category'))
    latitude = db.Column(db.Integer, nullable=False)   # location of place
    longitude = db.Column(db.Integer, nullable=False)
    instagram_place_id = db.Column(db.Integer, nullable=False)  # location of restuarant
    address = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        """Provide helpful information about the place."""

        return ("<Place place_id=%s place_name=%s>") % (self.place_id, self.place_name)


class LikedImage(db.Model):
    """Images users have liked associated with a Place"""

    __tablename__ = "LikedImages"

    liked_image_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('Places.place_id'), nullable=False)
    liked_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    visited = db.Column(db.Boolean, default=False, nullable=False)
    user_note = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.Text, nullable=False)

    ##define relationsip of user to images
    user = db.relationship("User", backref=db.backref("LikedImage", order_by=liked_image_id))
    place = db.relationship("Place", backref=db.backref("LikedImage", order_by=liked_image_id))

    def __repr__(self):
        """provide helpful information about restuarant and user information"""

        return "<LikedImages user_id=%s place_id=%s user_note=%s>" % (self.user_id,
                                                                      self.place_id,
                                                                      self.user_note)

class Category(db.Model):
    """Catergorize IG Photos"""

    __tablename__ = "Categories"

    category = db.Column(db.String(50), primary_key=True)  # increased string count

    def __repr__(self):
        """Provide helpful information about the image category"""

        return ("<Category category=%s>") % (self.category)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database (app is an instance and config is a dictionary)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forgetmenot.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
