from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from ..serializers import TagSerializer


TAGS_URL = reverse('recipe:tag-list')
# url for listing tags
# we're going to be using a view set so that automatically
# appends the action name to the end of the URL for us using
# the router.


class PublicTagsApiTests(TestCase):
    """Test the publicly available tags API"""
    # test that login is required for the API.

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required for retrieving tags"""
        res = self.client.get(TAGS_URL)
        # make a unauthenticated request to our tags URL
        # API or a tags API URL

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test the authorized user tags API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@londonappdev.com',
            'password'
        )
        # user we use for authenticating with
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        # make the request to the API
        # And then we're going to check that the tags
        # returned equal what we expect them to equal.
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        # ensures that the tags are returned in alphabetic order in reverse
        # order based on the name
        serializer = TagSerializer(tags, many=True)
        # many=True: more than one item in our serializer
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        # res.data is the data that was returned in the
        # response and we expect that to equal the serializer data
        # that we passed in so the
        # result should basically be the same and that should be a
        # reverse order list of tags
        # and all of them that are in the database ordered by name.

    def test_tags_limited_to_user(self):
        # we want to test that the tags that are retrieved are limited
        # just to the user that is logged in so we only want to see tags
        # that are assigned to the authenticated user.
        """Test that tags returned are for authenticated user"""
        # create a new user
        # in addition to the user that is created at the set up
        # just so we can assign a tag to that user and then we can
        # compare that that tag was not included in the response because
        # it was not the authenticated user.
        user2 = get_user_model().objects.create_user(
            'other@londonappdev.com',
            'testpass'
        )
        Tag.objects.create(user=user2, name='Fruity')
        tag = Tag.objects.create(user=self.user, name='Comfort Food')

        res = self.client.get(TAGS_URL)
        # we expect the one tag to be returned in the list because that's
        # the only tag assigned to the authenticated user

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        # length of the array that was returned in the request
        # and we want that to equal 1
        self.assertEqual(res.data[0]['name'], tag.name)
        # ake the first element of the data response

    def test_create_tag_successful(self):
        """Test creating a new tag"""
        # create a payload we're going to make the request and
        # then we're going to verify that the tag was created
        payload = {'name': 'Simple'}
        self.client.post(TAGS_URL, payload)

        # verify the tag exists
        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        # will return a boolean true or false
        self.assertTrue(exists)

# what happens if we create a tag with an invalid name
    def test_create_tag_invalid(self):
        """Test creating a new tag with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
