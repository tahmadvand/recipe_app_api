from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.conf import settings
# recommended way to retrieve
# different settings from the Django settings file

# These are all things that are required to extend the Django user
# model whilst making use of some of
# the features that come with the django user model out of the box.
# Create your models here.


class UserManager(BaseUserManager):
    # The manager class is a
    # class that provides the helper functions for creating a user or
    # creating a super user.

    def create_user(self, email, password=None, **extra_fields):
        # **extra_fields: take any of the extra functions that are passed
        # in when you call the create user and pass them into extra fields
        # makes our function a little more flexible
        """Creates and saves a new User"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        # Because we're only really going
        # to be using the create super user with the command-line we don't
        # need to worry about the extra fields.
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # assign the user manager to the objects attribute.
    objects = UserManager()
    # it creates a new user manager for our object.

    USERNAME_FIELD = 'email'
    # username and we're customizing that to email so we can use an email
    # address.


class Tag(models.Model):
    """Tag to be used for a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    # foreign key to our user object.

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient to be used in a recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    # create a foreign key to the auth user model
    # if we remove the user it will remove all the
    # recipes as well --> that's what cascade does
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    # you can allow it to be blank
    ingredients = models.ManyToManyField('Ingredient')
# This string here you can actually remove the quotes and just
# pass in the class directly The issue with this is you would
# have to then have your classes in the correct order.
# So if you remove the string around this reference to ingredient
# you would need to make sure the ingredient is above the recipe.

# Django has this useful feature where you can just provide the
# name of the class in a string and then it doesn't matter which
# order you place your models in.
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title
