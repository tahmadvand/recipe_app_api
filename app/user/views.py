from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer

# specify in this view is a class variable that points to the
# serializer class that we want to use to create the object

# this is the beauty of the Django rest framework it makes it really
# really easy for us to create APIs that do standard behavior like creating
# objects in the database.

# authentication view/our token view.


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for the user"""
    # it sets the renderer so we can view this
    # endpoint in the browser with the browsable api.
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

# create user or our manage user views.


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    # permissions are the level of access that the user has
    # user must be authenticated to use the API (they have to be logged in)

# get object function to our API view.
# API view is you would link it to a model and it could retrieve the item and
# you would retrieve data based models.
# In this case we're going to just get the
# model for the logged in user.
    def get_object(self):
        """"Retrieve and return authentication user"""
        return self.request.user
    # So when the get object is called the request will have the user
    # attached to it because of the authentication classes so because we
    # have the authentication class that takes care of take getting the
    # authenticated user and assigning it to request.
