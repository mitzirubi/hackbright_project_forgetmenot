"""Models and database functions for Forgetmenot project."""

from flask_sqlalchemy import SQLAlchemy
import datetime

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class Place(db.Model):
    """Places users have liked on IG Account stored in forgetmenot"""

    __tablename__ = "places"

    place_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    place_name = db.Column(db.String(200), nullable=True)  # because some photos may not have locations
    category = db.Column(db.String(50), db.ForeignKey('Categories.category'))
    latitude = db.Column(db.Integer, nullable=False)   # location of place
    longitude = db.Column(db.Integer, nullable=False)   # location of restuarant

    def __repr__(self):
        """Provide helpful information about the place."""

        return ("<Place place_id=%s user_id=%s \
                place_name=%s>") % (self.place_id,
                                    self.user_id, self.place_name)


class User(db.Model):
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


class LikedImages(db.Model):
    """Images users have liked associated with a Place"""

    __tablename__ = "liked_images"

    liked_image_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('images.place_id'), nullable=False)
    liked_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())  # is this the correct timestamp adder? yes
    visited = db.Column(db.Boolean, default=False, nullable=False)   # the date you visitied the location true or false instead
    image_url = db.Column(db.Text, nullable=False)
    user_note = db.Column(db.Text)

    ##define relationsip of user to images
    user = db.relationship("User", backref=db.backref("likes", order_by=liked_image_id))
    images = db.relationship("Images", backref=db.backref("likes", order_by=liked_image_id))
    #do i need a relationship of images ex: reaturant = db.relationship("Users", backbref=db.backfres("UserImageslikes"), order_by=created_at, )

    def __repr__(self):
        """provide helpful information about restuarant and user information"""

        return "<LikedImages user_id =%s place_id user_notes=%s>" % (self.user_id,
                                                                     self.place_id,
                                                                     self.user_notes)


class Category(db.Model):
    """Catergorize IG Photos"""

    __tablename__ = "categories"

    category = db.Column(db.String, primary_key=True)

    def __repr__(self):
        """Provide helpful information about the image category"""

        return ("<Category category=%s>") % (self.category)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database (app is an instance and config is a dictionary)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forgetmenot.db'   # created a new db link
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."

    app.run()
