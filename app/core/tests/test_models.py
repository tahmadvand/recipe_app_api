# our helper function for our model can create
# a new user.

from django.test import TestCase
from django.contrib.auth import get_user_model
from .. import models


#  makes it easy for us to create users in our test.
def sample_user(email='test@londonappdev.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        # test email
        email = 'test@londonappdev.com'
        password = 'Password123'
        user = get_user_model().objects.create_user(email=email,
                                                    password=password)

        # run some assertions to make sure that the user was created
        # correctly
        # checking: user.email == email
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        # password is encrypted, so we can check it using user.check_password

# As you can see here it says create user missing one required argument
# username this is because we haven't customized the user model and
# it's still expecting
# the standard username field that is required for the Django
# default user model.

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@LONDONAPPDEV.com'
        user = get_user_model().objects.create_user(email, 'test123')
        # random string for password
        # we already tested the password, we dont need to test it again

        self.assertEqual(user.email, email.lower())
        # makes the string lower case.

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    # The test is going to be to test that a super user is created
    # when we call create super user and that it is assigned
    # the is staff and the is super user settings.

    def test_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@londonappdev.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    # creates a tag and verifies that it converts to the correct string
    # representation.
    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            #  it calls sample user and creates a new user for
            # our test.
            name='Vegan'
            # give it a name of a tag we may use in
            # our system.
        )

        self.assertEqual(str(tag), tag.name)
        # it creates a
        # tag and then we just assert that when we convert our tag model
        # to a string it gives us the name.'

    def test_ingredient_str(self):
        # verify that the
        # ingredient model exists and that it work
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)
