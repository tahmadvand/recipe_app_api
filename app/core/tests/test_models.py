# our helper function for our model can create
# a new user.

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        # test email
        email = 'test@londonappdev.com'
        password = 'Password123'
        user = get_user_model().objects.create_user(
			email=email,
			password=password
		)

        # run some assertions to make sure that the user was created correctly
        # checking: user.email == email
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        # password is encrypted, so we can check it using user.check_password

## As you can see here it says create user missing one required argument username
#this is because we haven't customized the user model and it's still expecting
#the standard username field that is required for the Django default user model.

#
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