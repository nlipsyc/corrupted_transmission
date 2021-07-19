from django.urls import path

from .views import start_point

app_name = "calibration"
urlpatterns = [path("", start_point, name="start-point")]
