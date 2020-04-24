from rest_framework import serializers

from core.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag object"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_Fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for an ingredient object"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serialize a recipe"""
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )
    # it creates a primary key related field and
    # it says allow many and the query set that
    # we're going to use or that we're
    # going to allow to be part of this is going
    # to be from the ingredients.objects.all
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
    # point our
    # model serializer to the correct model
        fields = (
            'id', 'title', 'ingredients', 'tags', 'time_minutes', 'price',
            'link',
        )
    # fields that we want to return in our serializer
        read_only_fields = ('id',)
    # prevent the user from updating the ID when they
    # may create or edit requests

# we said that the difference between our list and our detail view
# would be that the detail one would specify the actual ingredients
# and the tag objects that are assigned to that recipe.
# Whereas this one(RecipeSerializer) as you can see it's using the
# primary key related field so it's only going to return the primary
# key or the ID of the ingredient and the tags associated to that recipe.


class RecipeDetailSerializer(RecipeSerializer):
    # (): base from recipeserializer
    # this means that the base of this is going to basically
    # be exactly the same
    """ Serialize a recipe detail """
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

# Django rest framework: you can nest serializers inside each other so we
# have one recipe detail sterilizer and then the related key object renders
# or returns the ingredients objects which we can then pass into our ingredient
# serializer and use that to convert it to this type of object.
