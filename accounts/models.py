from django.contrib.auth.models import AbstractBaseUser
from django.db import models


# Create your models here.


class User(AbstractBaseUser):
    GENDER_CHOICES = {
        "man": "Man",
        "female": "Female",
        "other": "Other"
    }

    birthday = models.DateField()
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
    email = models.EmailField()
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.BooleanField(
        default=False
    )
    is_active = models.BooleanField(
        default=True
    )
    is_superuser = models.BooleanField(
        default=False
    )

    USERNAME_FIELD = "email"

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff



