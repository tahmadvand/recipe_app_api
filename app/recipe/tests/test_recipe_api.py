from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
# use that for making our API requests

from core.models import Recipe, Tag, Ingredient

from ..serializers import RecipeSerializer, RecipeDetailSerializer

import tempfile
# allows you to call a function which will then create a temp file
# somewhere in the system and then you can remove that file after
# you've used it
import os
# this allows us to perform things like
# creating path names and also checking if files exist on the system
from PIL import Image
# pillow, this will import our image class which will let us then
# create test images which we can then upload to our API


RECIPES_URL = reverse('recipe:recipe-list')
# since we're going to need to access the URL in more
# or less all the tests let's assign that as a variable
# at top of the class in all capitals.
# app : identifier of the URL in the app

# /api/recipe/recipes
# /api/recipe/recipes/1/ (id) --> detail url


def image_upload_url(recipe_id):
    """Return URL for recipe image upload"""
    return reverse('recipe:recipe-upload-image', args=[recipe_id])
# generate our upload image url
# you're going to need the existing recipe ID in order to upload an image


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

# test partial update and full update of an object
# there are two ways in which you can update an object using the
# API there's two different HTTP methods: put, patch
# patch: Patch is used to update the fields that are provided
# in the payload so the only fields that it will change are the
# fields that are provided and any fields that are omitted from
# the request will not be modified in the object that's being updated.
    def test_partial_update_recipe(self):
        """Test updating a recipe with patch"""
    # make a request to change a field in our recipe.
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
    # add a tag to the recipe
        new_tag = sample_tag(user=self.user, name='Curry')
    # add a new tag and what we're going to do is we're going
    # to swap out this tag that we create here and we're going
    # to replace it with a new tag
        payload = {'title': 'Partially Updated sample recipe',
                   'tags': [new_tag.id]}
    # tags will be replaced with this new tag so the existing tag that
    # we created won't be assigned to it
        url = detail_url(recipe.id)
    # the way that you update an object using the Django rest framework
    # view sets is you use the detail URL so that is the URL of the
    # recipe with the ID of the recipe that we want to update.
        self.client.patch(url, payload)
    # make request
    # We're going to retrieve an update to the recipe from the
    # database and then we're going to check the fields that
    # are assigned and just make sure they match what we expect.

        recipe.refresh_from_db()
    # refreshes the details in our recipe from the database
    # typically when you create a new model and you have a
    # reference to a model the details of that won't change
    # unless you do refresh from dB if the values have changed
    # in the database.
        self.assertEqual(recipe.title, payload['title'])
        tags = recipe.tags.all()
        self.assertEqual(len(tags), 1)
        self.assertIn(new_tag, tags)
        #  check that the tag new tag is in the tags that we retrieved

    # test full update
    # put: it will replace the object that we're updating with the full
    # object that is provided in the request that means if you exclude
    # any fields in the payload those fields will actually be removed
    # from the object that you're updating
    def test_full_update_recipe(self):
        """Test updating a recipe with put"""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))

        payload = {
            'title': 'Fully Updated sample recipe',
            'time_minutes': 25,
            'price': 5.00
        }
        url = detail_url(recipe.id)
        self.client.put(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.time_minutes, payload['time_minutes'])
        self.assertEqual(recipe.price, payload['price'])
        tags = recipe.tags.all()
        self.assertEqual(len(tags), 0)
    # we will check that the tags assigned are zero now as I explained
    # because when we do a HTTP put if we omit a field
    # that should clear the value of that field so now our recipe
    # that did have a sample tag assigned should not have any tags
    # assigned


class RecipeImageUploadTests(TestCase):
    # what happens at the setup of the test
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user('user', 'testpass')
        self.client.force_authenticate(self.user)
    # authenticate our user
        self.recipe = sample_recipe(user=self.user)

    # after the test runs it runs tear down
    def tearDown(self):
        self.recipe.image.delete()
        # make sure that our file system is kept clean after our test
        # removing all of the test files that we create
        # delete the image if it exists in the recipe

    def test_upload_image_to_recipe(self):
        """Test uploading an image to recipe"""
        url = image_upload_url(self.recipe.id)
        # going to use the sample recipe that gets created

        # it creates a named temporary file on the system at a random
        # location usually in the /temp folder

        # create a temporary file we're going to write an image
        # to that file and then we're going to upload that file
        # through the API like you would with a HTTP POST and then
        # we're going to run some assertions to check that it
        # uploaded correctly
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            # creates black square
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            # it's the way that Python reads files so because we've
            # saved the file it will be the seeking will be done to the
            # end of the file so if you try to access it then it would
            # just be blank because you've already read up to the end
            # of the file so use this seek function to set
            # the pointer back to the beginning of the file
            res = self.client.post(url, {'image': ntf}, format='multipart')

        # assertions
        # refreshing the database for our recipe
        self.recipe.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # check that the images in the response so that's the path to
        # the image that should be accessible
        self.assertIn('image', res.data)
        # check that the path exists for the image that is saved to our model
        self.assertTrue(os.path.exists(self.recipe.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image"""
        url = image_upload_url(self.recipe.id)
        res = self.client.post(url, {'image': 'notimage'}, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
