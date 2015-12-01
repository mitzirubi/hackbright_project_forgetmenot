
## <a name="author"></a>About the author


Rubi graduated from UC Davis and was a fellow in Hackbright Cohort #12. She is a Software engineer with a background in customer support and exposure to the share economy and on demand delivery. She is a highly motivated, hardworking, and social individual who values opportunities that will foster learning and professional growth. For more details see her [linkedin] (https://www.linkedin.com/in/mitzirubimartinez) profile.

## Table of Contents
* [About the author](#author)
* [Technologies Used](#technologiesused)
* [App features](#features)
* [How to locally run Forgetmenot](#run)

# #Forgetmenot

Forgetmenot gives foodies the ability to keep track of the likes they want to remember, using the images geotag location. Users can enjoy checking places of their list and adding more liked images later.

![alt text](https://github.com/mitzirubi/hackbright_project_forgetmenot/blob/master/static/img/Readme/homepage.png "Homepage")

## <a name="features"></a>App features
This app has four main sections:
* __Favorites__, renders all the users instagram liked images that contain geotag locations. 
  ![alt text](https://github.com/mitzirubi/hackbright_project_forgetmenot/blob/master/static/img/Readme/favorites.png "Favorites")


* __Places Visited__, users can keep track of the locations they have vistied.
  ![alt text](https://github.com/mitzirubi/hackbright_project_forgetmenot/blob/master/static/img/Readme/placesvisited.png "Places Visited")


* __Forgetmenot Map__, renders all the users likes in a map view, it has a geolocation configuration so it knows where the user is located. The markers contain modal windows where they can be redirected to either google maps for directions or the Liked image information section.  
  ![alt text](https://github.com/mitzirubi/hackbright_project_forgetmenot/blob/master/static/img/Readme/forgetmenotmap.png "Forgetmenot Map")
  * __Forgetmenot Map window:__
  ![alt text](https://github.com/mitzirubi/hackbright_project_forgetmenot/blob/master/static/img/Readme/modalwindow.png "Modal window")

* __Likedimageinformation__, this feature provides a user with the location information for the liked image. They can see the liked image, the address information, a map of the location and write notes on their experience or keep track of their friends recommendations.
  ![alt text](https://github.com/mitzirubi/hackbright_project_forgetmenot/blob/master/static/img/Readme/placeinformation.png "image info")




## <a name="run"></a>How to locally run Forgetmenot

* Set up and activate a python virtualenv, and install all dependencies:
    * `pip install -r requirements.txt`
    * `source secrest.sh`
* Create the tables in your database:
    * `python -i model.py`
    * While in interactive mode, create tables: `db.create_all()`
* Next, seed your data (you must have an Instagram API key(remember to source your secrets!) before running your seed file. In this seed file you will make a request to both Instagram and google maps. Which will request the user liked images, and commit them to your database(WIP: OAuth):
   * `python seed.py`
* Start up the flask server:
    * `python server.py`

* Go to localhost:5000 to see the web app



## <a name="technologiesused"></a>Technologies Used

* Python
* Sqlite3
* Sqlalchemy
* Flask
* Javascript
* JQuery
* AJAX
* JSON
* Jinja2
* Bootstrap
* Instagram API
* Google Maps API 

(dependencies are listed in requirements.txt)


