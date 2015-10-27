"""Models and database functions for Forgetmenot project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class Restaurants(db.Model):
    """Restaurants users have liked on IG Account stored in Forgetmenot"""

    __tablename__ = "restaurants"

restaurant_id = db.Column(db.Interger, autoincrement=True, Primary_key=True)
user_id = db.Column(db.Interger, db.ForeignKey('Users.user_id'))
restaurant_name = db.Column(db.String(200), nullable=True)  #because some photos may not have locations
latitude = db.Column(db.Interger)  #location of restaurant
longitude = db.Column(db.Interger)  #location of restuarant
image_url = db.Column(db.String(200), nullable=False)
thumbnale_url = db.Column(db.String(200), nullable=False)
user_notes = db.Column(db.String(2500), nullable=True) ##ask about string or characters that can be used.
date_added = db.Column(db.DateTime, nullable=True) #is this the correct timestamp adder?
visited = db.Column(db.DateTime, nullable=True)  #the date you visitied the location
category_id = db.Column(db.Interger, db.ForeignKey ('Catergories.category_id'))

    def __repr__(self):
        """Provide helpful information about the restaurant."""

        return "<Restaurant restaurant_id=%s user_id=%s restaurant_name=%s"> %(self.restaurant_id,
                                                                               self.user_id, self.restaurant_name) 
                                                    

