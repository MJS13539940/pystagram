from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# AbstractUser의 필드들
#   username
#   password
#   first_name
#   last_name
#   email
#   is_staff
#   is_active
#   date_joined
#   last_login

class User(AbstractUser):
    profile_image = models.ImageField("프로필 이미지", upload_to="users/profile", blank=True)
    short_description = models.TextField("소개글", blank=True)

