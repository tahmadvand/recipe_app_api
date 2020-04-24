from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
# use that for making our API requests

from core.models import Recipe, Tag, Ingredient

from ..serializers import RecipeSerializer, RecipeDetailSerializer


RECIPES_URL = reverse('recipe:recipe-list')
# since we're going to need to access the URL in more
# or less all the tests let's assign that as a variable
# at top of the class in all capitals.
# app : identifier of the URL in the app

# /api/recipe/recipes
# /api/recipe/recipes/1/ (id) --> detail url


def detail_url(recipe_id):
    """Return recipe detail URL"""
    return reverse('recipe:recipe-detail', args=[recipe_id])
# name of the end point that the default router will create
# for our viewset because we're going to have a detail action

# this is how you specify arguments with the reverse function
# you just pass in args and then you pass in a list of the
# arguments you want to add
# here we have single item


def sample_tag(user, name='Main course'):
    """Create and return a sample tag"""
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name='Cinnamon'):
    """Create and return a sample ingredient"""
    return Ingredient.objects.create(user=user, name=name)


def sample_recipe(user, **params):
    """Create and return a sample recipe"""
    defaults = {
        'title': 'Sample recipe',
        'time_minutes': 10,
        'price': 5.00,
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)
# convert the dictionary into the argument
# when you use the two asterisks when calling a
# function it has the reverse effect.


class PublicRecipeApiTests(TestCase):
    """Test unauthenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()

    def test_required_auth(self):
        """Test the authenticaiton is required"""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """Test authenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@londonappdev.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving list of recipes"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)
    # we're going to access them by retrieving
    # all of the recipes from our database.

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """Test retrieving recipes for user"""
        # test recipes are limited to the authenticated user.
        user2 = get_user_model().objects.create_user(
            'other@londonappdev.com',
            'pass'
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)
    # filter our recipes by the authenticated user

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
    # many=true: this is because we were returning the list view
    # or we wanted to simulate the list view in our serializer
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_recipe_detail(self):
        """Test viewing a recipe detail"""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
    # in this case we just want to serialize a single object
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_recipe(self):
        """Test creating recipe"""
        payload = {
            'title': 'Test recipe',
            'time_minutes': 30,
            'price': 10.00,
        }
        res = self.client.post(RECIPES_URL, payload)
    # post this payload dictionary to our recipes URL.

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    # this is the standard HTTP response code for creating objects
    # in an API.
        recipe = Recipe.objects.get(id=res.data['id'])
    # When you create an object using the Django rest framework the
    # default behavior is that it will return a dictionary containing
    # the created object This is how I know that if we do res.data and
    # retrieve the id key this will get the id of the created object.

    # Next what we're going to do is we're going to loop through each
    # one of these keys and then we're going to check
    # that is the correct value assigned to our recipe model.
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))
        # assertion for each one of these keys, check that it is
        # equal to the same key in the recipe
        # payload[key]: This will actually get the value of the
        # key in our payload object
        # getattr: that allows you to retrieve an attribute from
        # an object by passing in a variable. (instead of recipe.key)

    def test_create_recipe_with_tags(self):
        """Test creating a recipe with tags"""
        tag1 = sample_tag(user=self.user, name='Tag 1')
        tag2 = sample_tag(user=self.user, name='Tag 2')
        payload = {
            'title': 'Test recipe with two tags',
            'tags': [tag1.id, tag2.id],
            'time_minutes': 30,
            'price': 10.00
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        # retrieve the created recipe
        tags = recipe.tags.all()
        # retrieve the tags that were created with the recipe
        self.assertEqual(tags.count(), 2)
        # because we expect two tags to be assigned.
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)
    # check if the tags that we created as our sample tags are
    # the same as the tags that are in our queryset.

    def test_create_recipe_with_ingredients(self):
        """Test creating recipe with ingredients"""
        ingredient1 = sample_ingredient(user=self.user, name='Ingredient 1')
        ingredient2 = sample_ingredient(user=self.user, name='Ingredient 2')
        payload = {
            'title': 'Test recipe with ingredients',
            'ingredients': [ingredient1.id, ingredient2.id],
            'time_minutes': 45,
            'price': 15.00
        }

        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        ingredients = recipe.ingredients.all()
        # get the ingredients queryset
        self.assertEqual(ingredients.count(), 2)
        self.assertIn(ingredient1, ingredients)
        self.assertIn(ingredient2, ingredients)
