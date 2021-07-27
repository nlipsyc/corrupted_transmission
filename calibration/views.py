from decimal import Decimal
from math import sqrt
from typing import Tuple
import json

import reverse_geocode
from corrupted_transmission.utils import Coordinate
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# Altitude is the mathy word for height. This coresponds to roughly 1.11km of latitude
# Don't change this, the values to account for the longitude expansion at this longitude are based off this
# Yes this is hacky, no I don't care.
TRIANGLE_ALTITUDE = Decimal(0.01)


def start_point(request):
    response = HttpResponse()
    latitude = request.GET.get("y", "0")
    longitude = request.GET.get("x", "0")

    try:
        float(latitude)
        float(longitude)
    except ValueError:
        # This is the one time in my life I actually _want_ cryptic error messages
        return HttpResponse("Error! XY does not compute.")

    # Correct params input, go to next step
    success_link = reverse("calibration:triangulation")

    city_name = reverse_geocode.search(((latitude, longitude),))[0]["city"]
    country_name = reverse_geocode.search(((latitude, longitude),))[0]["country"]

    # TODO write some tests for this

    if float(latitude) == 0 and float(longitude) == 0:
        location_message = "Null island does not exist"
        response.write(location_message)

    elif city_name == settings.CITY_NAME:
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
    center_point: Coordinate, altitude: Decimal = TRIANGLE_ALTITUDE
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
    return render(request, "triangulation.html")


@csrf_exempt
def triangulate(request):
    """Called to calculate distance from each triangle point."""
    # Derived experimentally
    zeroing_values = [Decimal("0.005"), Decimal("0.007637626"), Decimal("0.007637626")]
    # This should require actual entry into the location (within ~100m).
    location_tolerance = Decimal("0.0008")

    browser_geolocation = json.loads(request.POST.get("coordinates"))
    current_location = Coordinate(browser_geolocation["y"], browser_geolocation["x"])
    destination: Coordinate = settings.ECOLOGICAL_PRESERVE

    triangulation_vertices = _generate_equilateral_triangle_around_point(destination)
    distances_from_vertices = [current_location - vertex for vertex in triangulation_vertices]
    vertex_names = ["a", "b", "c"]

    # These magic numbers (zeroing_values), when combined with the TRIANGLE_ALTITUDE, at the latitude of the
    # ECOLOGICAL_PRESERVE will 0 out our distances when we arrive. At the equator they'd all be the same, but maps
    # stretch at the poles. Doing this properly would involve bringing in a mapping API which is silly
    zeroed_distances = [vertex - correction for (vertex, correction) in zip(distances_from_vertices, zeroing_values)]
    absolute_zeroed_distances = [abs(d) for d in zeroed_distances]

    is_arrived_at_destination = all([distance < location_tolerance for distance in absolute_zeroed_distances])

    # Return the difference for each point.  Multiply by 1000 and truncate to 6 places for easier legibility.
    formated_vertices = dict(zip(vertex_names, [round(v * 1000, 6) for v in absolute_zeroed_distances]))

    context = {}
    context.update(formated_vertices)
    context.update({"is_arrived": is_arrived_at_destination})

    return render(request, "partial_triangulate.html", context)
