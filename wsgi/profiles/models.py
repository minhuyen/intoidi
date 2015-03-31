from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from pybb.profiles import PybbProfile

from pybb.compat import get_user_model_path, get_username_field
from django.core.urlresolvers import reverse


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        email = BaseUserManager.normalize_email(email)
        user = self.model(username=username, email=email, is_staff=False, is_active=True, is_superuser=False)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        email = BaseUserManager.normalize_email(email)
        user = self.model(username=username, email=email, is_staff=True, is_active=True, is_superuser=True)

        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('username', unique=True, max_length=100)
    email = models.EmailField('email')
    is_staff = models.BooleanField('staff', default=False)
    is_active = models.BooleanField('active', default=True)
    date_joined = models.DateTimeField('date joined', default=timezone.now)
    description = models.TextField('description', default="")

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    class Meta:
        abstract = False


class CustomProfile(PybbProfile):
    user = models.OneToOneField(get_user_model_path(),
                                verbose_name='linked account',
                                related_name='pybb_customprofile',
                                blank=False, null=False,)

    class Meta(object):
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def get_absolute_url(self):
        return reverse('pybb:user', kwargs={'username': getattr(self.user, get_username_field())})

    def get_display_name(self):
        return self.user.get_username()