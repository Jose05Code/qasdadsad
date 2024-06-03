from django.urls import path
from . import views
from .views import send_picture
from .views import ItemList

urlpatterns = [
    path('pictures/<str:name>/', send_picture, name='send_picture'),
    path('items/', ItemList, name='item_list')
    # Add more paths here
]