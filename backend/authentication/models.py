#models.py
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import jwt,datetime
from django.utils import formats


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        # Set a default username if it's not provided
        extra_fields.setdefault('username', email)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, name, password, **extra_fields)


class User(AbstractUser):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=50, null=True, blank=True)  # Add this line

    # password = models.CharField(max_length=100)
    first_name = None
    last_name = None
    
    objects = CustomUserManager()  # Use the custom user manager

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def is_logged_in(self):
        # Check if the user is currently logged in
        return self.is_authenticated

    is_logged_in.boolean = True  # Display as a boolean field in the admin


    @property
    def get_jwt_token(self):
        payload = {
            'id': self.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token
