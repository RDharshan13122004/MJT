from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('login/', user_login, name='user_login'),
    path('signup/', signup, name='signup'),
]