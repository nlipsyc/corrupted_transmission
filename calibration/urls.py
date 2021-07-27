from django.urls import path

from .views import start_point, triangulation, triangulate

app_name = "calibration"
urlpatterns = [
    path("", start_point, name="start-point"),
    path("triangulation/", triangulation, name="triangulation"),
    path("triangulate/", triangulate, name="triangulate"),
]
