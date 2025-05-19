from django.urls import path
from menu.views import menu_view


urlpatterns = [
    path('', menu_view, name='menu'),
]
