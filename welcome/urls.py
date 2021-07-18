from django.urls import path

from .views import home_page

app_name = "welcome"
urlpatterns = [path("", home_page)]
