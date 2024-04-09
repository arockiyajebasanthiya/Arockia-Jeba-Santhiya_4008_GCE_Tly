from django.urls import path
from polls.views import index  # Import the index view function from the polls app

urlpatterns = [
    path('', index, name='index'),  # Use the index view function from the polls app
    # Other URL patterns for the pages app
]
