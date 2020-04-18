# This is where we're going to store our serializers for our user. (model serializer)
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
# whenever you're outputting any messages
# in the Python code that are going to be output to the screen it's a good idea to
# pass them through this translation system just so if you ever do add any
# extra languages to your projects you can easily add the language file and it will
# automatically convert all of the text to the correct language.


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        # (): because we want to call the get user model so it actually
        # returns the user model class
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
        # keyword args

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)
    # **: unwind this validated data into
    # the parameters of the create user function.

    # make sure the password is set using the set
    # password function instead of just setting it to whichever value is
    # provided.
    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        # remove the password from the validated data (pop), None: default value
        user = super().update(instance, validated_data)
        # super we'll call the model
        # serializers update functions, so the default one, it will call the default
        # function in our function so we can make use of all the functionality that's
        # included in the default one whilst extending it slightly to customize it
        # for our needs.
        if password:
            # if user provides a password
            user.set_password(password)
            user.save()

        return user


# so what Django rest framework does is when we're ready to create the user it
# will call this create function and it will pass in the
# validated data the validated data will contain all of the data that was passed
# into our serializer which would be the JSON data that was made in the HTTP POST
# and it passes it as the argument here and then we can then use that to create our user

    # authenticating our requests.
class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
        # there shouldn't be whitespace before or after your password
        # Django rest framework serializer it will trim it off
    )

# we're just modifying rest framework slightly to accept our email address
# instead of username.
    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        # access the context of the
        # request that was made so we're going to pass this into our view set and what the
        # Django rest framework view set does is when a request is made it passes the
        # context into the serializer in this context class variable
        if not user:
            # if we dont return a user, authentication failure
            msg = _('Unable to authenticate with provided credentials')
            # _ calling our translation function
            raise serializers.ValidationError(msg, code='authorization')
            # handle the error

        attrs['user'] = user
        return attrs
    # whenever you're overriding the validate
    # function you must return the values at the end once the validation is
    # successful.
