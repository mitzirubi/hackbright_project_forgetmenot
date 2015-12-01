function initMap() {
      var map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 37.7833, lng: -122.4167 },
        zoom: 11
      });

      var infoWindow = new google.maps.InfoWindow({map: map});

      // Try HTML5 geolocation.
      if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
              var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
              };

              infoWindow.setPosition(pos);
              infoWindow.setContent('You are here!');
              map.setCenter(pos);
            }, function() {
              handleLocationError(true, infoWindow, map.getCenter());
            });
      }

      else {
        // Browser doesn't support Geolocation
            handleLocationError(false, infoWindow, map.getCenter());
      }

    function handleLocationError(browserHasGeolocation, infoWindow, pos) {
      infoWindow.setPosition(pos);
      infoWindow.setContent(browserHasGeolocation ?
                            'Error: The Geolocation service failed.' :
                            'Error: Your browser doesn\'t support geolocation.');

    
    }

      $.get('/map_photo_info.json', function (place) {
                  
      var placeArray = place.places;
      var place, marker, html;

      for (var i = 0; i < placeArray.length; i++) {
            place = placeArray[i];

          // Define the marker
          marker = new google.maps.Marker({
              position: new google.maps.LatLng(place.latitude, place.longitude),
              map: map,
              icon: '/static/img/asterisco.png',
              id: 'place ID: ' + place.placeId,
              draggable: false,
              visited: place.visited,
              user_note: place.user_note,
              title:'Place Name: ' + place.placeName
             
          });

          // Define the content of the infoWindow
          html = (
              '<div class="window-content">' +
                  '<img src="'+ place.imageUrl +'"alt="favoriteplaces" style="width:150px;" class="thumbnail">' +
                  '<p><b>Place name: </b><a href="/likedimageinfo/'+ place.placeId +'" > ' + place.placeName + '</a></p>' +
                  '<p><b>Visited?: </b>' + place.visited + '</p>' +
                  '<p><b>Notes: </b>' + place.user_note + '</p>' +
                  '<p><b>Location: </b><a id="place-address" href="http://maps.google.com/?q='+ place.address + '" target="_blank"> ' + place.address + '</a></p>' +
              '</div>');

          // Inside the loop we call bindInfoWindow passing it the marker,
          // map, infoWindow and contentString
          bindInfoWindow(marker, map, infoWindow, html);
      }

  });
}

  // This function is outside the for loop.
  // When a marker is clicked it closes any currently open infowindows
  // Sets the content for the new marker with the content passed through
  // then it open the infoWindow with the new content on the marker that's clicked
  function bindInfoWindow(marker, map, infoWindow, html) {
      google.maps.event.addListener(marker, 'click', function () {
          infoWindow.close();
          infoWindow.setContent(html);
          infoWindow.open(map, marker);
      });
  }

//close init

 google.maps.event.addDomListener(window, 'load', initMap);








