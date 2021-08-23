import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User Model
    """

    ROLE_USER = 'user'
    ROLE_MODERATOR = 'moderator'
    ROLE_ADMIN = 'admin'
    ROLES = [
        (ROLE_USER, 'user'),
        (ROLE_MODERATOR, 'moderator'),
        (ROLE_ADMIN, 'admin')]

    email = models.EmailField(
        verbose_name='email address',
        help_text='email address',
        max_length=254,
        unique=True)

    bio = models.TextField(
        max_length=256,
        blank=True,
        null=True
    )
    role = models.CharField(
        max_length=16,
        choices=ROLES,
        default=ROLE_USER,
        null=False)
    confirmation_code = models.UUIDField(
        editable=False,
        default=uuid.uuid4
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    @property
    def is_user(self):
        return self.role == self.ROLE_USER

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.ROLE_MODERATOR or self.is_admin
