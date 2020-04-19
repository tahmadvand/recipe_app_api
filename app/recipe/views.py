from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag

from . import serializers


class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage tags in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    # his requires that token authentication is used and the
    # user is authenticated to use the API
    queryset = Tag.objects.all()
    # query set we want to return
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        # override the get query set function
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')
    # when our viewset is invoked from a URL
    # it will call get_queryset to retrieve these objects and this
    # is where we can apply any custom filtering like limiting it to
    # the authenticated user

    # authentication is required
