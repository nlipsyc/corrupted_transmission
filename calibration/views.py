import reverse_geocode

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse


def start_point(request):
    response = HttpResponse()
    latitude = request.GET.get("y", "0")
    longitude = request.GET.get("x", "0")

    # Correct params input, go to next step
    # TODO put in the triangulation link here
    success_link = reverse("calibration:start-point")

    city_name = reverse_geocode.search(((latitude, longitude),))[0]["city"]
    country_name = reverse_geocode.search(((latitude, longitude),))[0]["country"]

    # TODO write some tests for this

    if float(latitude) == 0 and float(longitude) == 0:
        location_message = "Null island does not exist"
        response.write(location_message)

    elif city_name == "Guelph":
        location_message = "Location acquired, commence triangulation"
        response.write(f'<a href="{success_link}">{location_message}</a>')

    else:
        location_message = (
            f"Location of {city_name}, {country_name} does not match background stelar data.  Please try again."
        )
        response.write(location_message)

    # Carve out to get this joke in

    return response
