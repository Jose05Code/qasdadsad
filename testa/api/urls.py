from django.urls import path
from . import views
from .views import send_picture

urlpatterns = [
    path('pictures/<str:name>/', send_picture, name='send_picture'),
    # Add more paths here
]