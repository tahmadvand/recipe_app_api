from rest_framework.decorators import action
# add custom actions to your view set
from rest_framework.response import Response
# this is for returning a custom response

from rest_framework import viewsets, mixins, status
# check the status we're going to use it to generate a
# status for our custom action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe

from . import serializers

# we're going to base our new class off the common base classes
# that the ingredients and the tags use so that is viewsets.
# for reducing duplicates between tag and ingredients api
# for making each view set unique


class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """Base viewset for user owned recipe attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new ingredient"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


# class TagViewSet(viewsets.GenericViewSet,
#                  mixins.ListModelMixin,
#                  mixins.CreateModelMixin):
#     """Manage tags in the database"""
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     # his requires that token authentication is used and the
#     # user is authenticated to use the API
#     queryset = Tag.objects.all()
#     # query set we want to return
#     serializer_class = serializers.TagSerializer
#
#     def get_queryset(self):
#         # override the get query set function
#         """Return objects for the current authenticated user only"""
#         return self.queryset.filter(user=self.request.user).order_by('-name')
#     # when our viewset is invoked from a URL
#     # it will call get_queryset to retrieve these objects and this
#     # is where we can apply any custom filtering like limiting it to
#     # the authenticated user
#
#     # authentication is required
#
#     # override the perform create so that we can assign the
#     # tag to the correct user.
#     def perform_create(self, serializer):
#         """Create a new ingredient"""
#         serializer.save(user=self.request.user)
#         # set the user to the authenticated user.
#
#
# class IngredientViewSet(viewsets.GenericViewSet,
#                         mixins.ListModelMixin,
#                         mixins.CreateModelMixin):
#     """Manage ingredients in the database"""
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
# # make sure all
# # the users that use this API are authenticated
#     queryset = Ingredient.objects.all()
# # (): call the all function
#     serializer_class = serializers.IngredientSerializer
#
#     def get_queryset(self):
#         """Return objects for the current authenticated user only"""
#         return self.queryset.filter(user=self.request.user).order_by('-name')
#
#     def perform_create(self, serializer):
#         """Create a new ingredient"""
#         serializer.save(user=self.request.user)


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    # allow them to
    # update and to create and to view details
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the recipes for the authenticated user"""
        return self.queryset.filter(user=self.request.user)

# rest framework documentation: this is the function that's called
# to retrieve the serializer class for a particular request
# and it is this function that you would use if you wanted to change
# the serializer class for the different actions that are available on
# the recipe viewset

# we have a number of actions available by default in the model viewset
# one of them is list in which case we just want to return the default
# and the other action is retrieve in which case we want to return the
# detail sterilizer so then when you call the retrieve action it
# serializes it using that serializer instead of the default one

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        # name of the function is important to work correctly
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class
# if the action is retrieve and we want to return the default,
# the recipe detail sterilizer otherwise this won't
# be called and it will just return the normal serializer class

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)

# ModelViewSet allows you to create objects out of the box
# So with the default functionality of it is if you pass a
# serializer class and it's assigned to a model then it
# knows how to create new objects with that model when you
# do a HTTP POST.
# So the only thing we need to do is assign the authenticated
# user to that model once it has been created.

    # add custom actions
    @action(methods=['POST'], detail=True, url_path='upload-image')
    # method:post,put,patch, post:post an image to our recipe
    # url_path:path that is visible within the URL
    def upload_image(self, request, pk=None):
        # pk:primary key that is passed in with the URL
        # so it gets passed into the view as PK
        """Upload an image to a recipe"""
        recipe = self.get_object()
        # retrieve the recipe object
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )
        # get the serializer and we pass in our recipe and the
        # data is going to be the request.data

        if serializer.is_valid():
            # makes sure that the image field is correct and
            # that no other extra fields have been provided
            serializer.save()
            return Response(
                serializer.data,
                # id
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            # this will return the errors for the serializer
            # these are automatically generated by the
            # Django rest framework
            status=status.HTTP_400_BAD_REQUEST
        )
