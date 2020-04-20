#  admin page unit tests.

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
# allow us to generate URLs for our Django admin page.
from django.test import Client
# will allow us to make test requests to our application in our unit tests.


class AdminSiteTests(TestCase):

    def setUp(self):
        # it is a function that is ran before every test that we
        # run so sometimes there are setup tasks that need to be done
        # before every test in our test case class.
        self.client = Client()
        # create test client
        # add a new user that we can use to test we're going
        # to make sure the user is logged into our client and finally
        # we're going to create a regular user that is not authenticated
        # or that we can use to list in our admin page.
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@londonappdev.com',
            password='password123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@londonappdev.com',
            password='password123',
            name='Test User Full Name',
        )

        # so what this does is it uses the client helper function that
        # allows you to log a user in with the Django authentication and
        # this really helps make our tests a lot easier to write because
        # it means we don't have to manually log the user in we can just
        # use this helper function.

    def test_users_listed(self):
        """Test that users are listed on the user page"""
        url = reverse('admin:core_user_changelist')
        # generate the URL for our list user page.
        # the reason we use this reverse function instead of
        # just typing the URL manually is because
        # if we ever want to change the URL in a future it means
        # we don't have to go through and change it everywhere in our
        # test because it should update
        # automatically based on reverse.
        res = self.client.get(url)
        # response
        # This will use our test client to perform a HTTP GET on
        # the URL that we have found here.

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
        # check that our response here contains a certain item.

        # it looks into the actual content of this res because if you
        # were to manually output this res it's just an object so it's
        # intelligent enough to look into the actual output that is
        # rendered and to check for the contents there

# test for is we're just going to test that the change page renders correctly.
    def test_user_page_change(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        #  what this does is the reverse function will create a URL like this
        # /admin/core/user/id
        # this is how the arguments function or the arguments argument works
        # in the reverse function.
        res = self.client.get(url)
        # we're going to do an HTTP get on the URL

        self.assertEqual(res.status_code, 200)
        # what we test here is that a
        # status code for the response that our client gives is HTTP 200
        # which is the
        # status code for okay so that means HTTP 200 okay the page worked.

    # This is the page for adding new users in the Django admin.
    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
