from decimal import Decimal
from corrupted_transmission.utils import Coordinate
from typing import Tuple
from math import sqrt
import reverse_geocode
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse


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


def _generate_equilateral_triangle_around_point(
    center_point: Coordinate, altitude: Decimal
) -> Tuple[Coordinate, Coordinate, Coordinate]:
    """Given a center point, generate a triangle around it.

    This will generate a north (a), south-east(b) and south-west(c) point that form an equilateral triangle around the
    center point. The height of the triangle (apparently the math word is "altitude") is specified in degrees.
    """
    # This is how you math I guess?
    side_length = 2 * altitude / Decimal(sqrt(3))

    ay = center_point.y + altitude / 2
    ax = center_point.x
    a = Coordinate(ay, ax)

    by = center_point.y - altitude / 2
    bx = center_point.x + side_length / 2
    b = Coordinate(by, bx)

    cy = center_point.y - altitude / 2
    cx = center_point.x - side_length / 2
    c = Coordinate(cy, cx)

    return (a, b, c)


def triangulation(request):
    ...
