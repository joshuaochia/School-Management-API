from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
    )


class UserManager(BaseUserManager):

    def create_user(
        self, email, first_name, middle_name,
        last_name, password, **kwargs
    ):

        if not email:
            raise ValueError('User must have email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, first_name,
        last_name, middle_name, password
    ):

        user = self.create_user(
            email, first_name, last_name,
            middle_name, password
            )

        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):

    """ Main User config """
    email = models.EmailField(unique=True, verbose_name='Email Address')
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'middle_name']

    objects = UserManager()

    class Meta:
        db_table = 'user_profile'

    def __str__(self):

        return f'{self.first_name} {self.last_name}'

    def has_perm(self, perm, obj=None):
        # User permission
        return True

    def has_module_perms(self, app_label):
        # User permission to view the ap modules
        return True
