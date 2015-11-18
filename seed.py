import model
import requests
import pprint
import os

printer = pprint.PrettyPrinter()
access_token = os.environ['ACCESS_TOKEN']
geocode_key = os.environ['GEOCODE_KEY']



def store_user_info():
    """Retrieve user information from Instagram API and store it into our database."""

    model.User.query.delete()
    model.Place.query.delete()
    model.LikedImage.query.delete()


    results = requests.get('https://api.instagram.com/v1/users/self?access_token=%s' % (access_token))
    printer.pprint(results.json())

    # results.json() #gives me the class json
    #we assign it to a veriable and it becomes a dictionary
    results = results.json()

    #result is only 1 dictionary no need to loop
    r = results['data']

    username = r['username']
    profile_picture = r['profile_picture']

                            # model  vs variable that I am passing
    user = model.User(username=username, profile_picture=profile_picture)  # this will need access key etc.

    model.db.session.add(user)

    model.db.session.commit()

    results = requests.get('https://api.instagram.com/v1/users/self/media/liked?access_token=%s' % (access_token))
    printer.pprint(results)

    results = results.json()

    object_information = results['data']

    for liked_image in object_information:

        location_data = liked_image['location']

        if location_data:
            latitude = location_data['latitude']
            longitude = location_data['longitude']
            place_name = location_data['name']
            instagram_place_id = location_data['id']

            image_url = liked_image['images']['standard_resolution']['url']

            print 'image_url: ', image_url

            geocode_info = requests.get(("https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&key={}").format(latitude, longitude, geocode_key))

            geocode_results = geocode_info.json()

            geo_code = geocode_results['results']

            locationx = geo_code[0]

            address = locationx['formatted_address']


            # Is there already a place with this instagram place id? if yes, dont add
            place = model.Place.query.filter_by(instagram_place_id=instagram_place_id).first()

            if not place:

                place = model.Place(place_name=place_name, latitude=latitude, longitude=longitude,
                                    instagram_place_id=instagram_place_id, address=address)

                model.db.session.add(place)
                model.db.session.commit()

            liked_image = model.LikedImage(user_id=user.user_id, place_id=place.place_id, image_url=image_url)

            model.db.session.add(liked_image)

    model.db.session.commit()

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    model.connect_to_db(app)
    print "Connected to DB."

    store_user_info()
