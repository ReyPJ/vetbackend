from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class CustomUser(AbstractUser):
    ADMIN = 'admin'
    STAFF = 'staff'
    MEMBER = 'member'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (STAFF, 'Staff'),
        (MEMBER, 'Member'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=MEMBER)
    phone = models.CharField(max_length=12, blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
        related_query_name='customuser',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
        related_query_name='customuser',
    )

