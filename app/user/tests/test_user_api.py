from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
# so we can generate our API URL.

# rest framework test helper tools:
from rest_framework.test import APIClient
# test client that we can use to make requests to our API and then
# check what the response is.
from rest_framework import status
# a module that contains some status codes that we can see in basically human
# readable form so instead of just typing 200 it's HTTP 200 ok it just makes the
# tests a little bit easier to read and understand.

# add a helper function or a
# constant variable for our URL that we're going to be testing so we're
# be testing the create user URL:
CREATE_USER_URL = reverse('user:create')
# create the user
# create URL and assign it to this create user URL variable.
TOKEN_URL = reverse('user:token')
# this is going to be the URL that we're going to use to make the HTTP
# POST request to generate our token.


def create_user(**params):
    # **: dynamic list of arguments.
    # we can basically add as many arguments as we want
    """Helper function to create new user that you're testing with"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)(unauthenticated)"""

    def setUp(self):
        self.client = APIClient()
    # this just makes it a little easier
    # to call our client in our test so every single test we run we don't need to
    # manually create this API client we just have one client for our test suite that
    # we can reuse for all of the tests.

    def test_create_valid_user_success(self):
        """Test creating using with a valid payload is successful"""
        # payload is the object that you pass to
        # the API when you make the request
        payload = {
            'email': 'test@londonappdev.com',
            'password': 'testpass',
            'name': 'name',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        # make request
        # do a HTTP POST request to our client
        # to our URL for creating users

        # test that the outcome is what we expect: http 201 is created
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # test that the object is actually created
        user = get_user_model().objects.get(**res.data)
        # here is we can unwind the response for this because when we do a HTTP POST and
        # create a user we expect to see the created user object returned in the
        # API along with this HTTP_201_created
        # So if we do **res.data then it will take the dictionary response
        # which should look very similar to this but it should have an added ID field
        # We take the res.data and we just pass it in as the parameters for the get then
        # if this gets the user successfully then we know that the user is actually being
        # created properly.

        self.assertTrue(
            user.check_password(payload['password'])
            # test our password is correct
        )
        self.assertNotIn('password', res.data)
        # we don't want the password
        # being returned in the request because it is a potential security vulnerability.
        # password shouldn't be returned when we return our user

    def test_user_exists(self):
        """Test creating a user that already exists failure"""
        payload = {'email': 'test@londonappdev.com', 'password': 'testpass', 'name': 'Test'}
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # make sure it's a bad request because the user already exists

    def test_password_too_short(self):
        """Test that password must be more than 5 characters"""
        payload = {'email': 'test@londonappdev.com', 'password': 'pw', 'name': 'Test'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        # if the user exists it will return true otherwise it will return false
        self.assertFalse(user_exists)

# every single test that runs it refreshes the database
# so these users that were created in this test are not going to be accessible in
# this test so each test it basically starts anew

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {'email': 'test@londonappdev.com', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        # response
        # make a request to post payload to our token_url

        self.assertIn('token', res.data)
        # checks that there is a key called token in the response.data that we get back.
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='test@londonappdev.com', password='testpass')
        payload = {'email': 'test@londonappdev.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # because the password is wrong

    def test_create_token_no_user(self):
        """Test that token is not created if user doens't exist"""
        payload = {'email': 'test@londonappdev.com', 'password': 'testpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

# because each test it resets the database
# from scratch we don't need to worry about the fact that we created the user
# in this test because this test is going to run isolated from this test and the
# user won't exist by the time we start this test.
