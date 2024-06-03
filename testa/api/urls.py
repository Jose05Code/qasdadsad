from django.urls import path
from . import views
from .views import item_pictures
from .views import ItemList
urlpatterns = [
    path('items/', ItemList, name='item_list'),
    path('item_picture/<str:name>/', item_pictures, name='send_picture'),
]