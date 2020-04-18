from django.urls import path
# allows us to define different paths in our app.
from . import views
# define our app name and
# the app name is set to help identify which app we're creating the URL from
# when we use our reverse function that you would have seen in the tests we've
# used it multiple times so far.
app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
]