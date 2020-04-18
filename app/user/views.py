from rest_framework import generics
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
