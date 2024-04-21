from django.db import models
from djongo.models.fields import Model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# Create your models here.

class customer(Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100 , blank = True , null = True)
    email = models.EmailField(blank=True,null=True)
    assets_type = models.CharField(max_length=20,blank=True,null=True)
    assign = models.BinaryField(blank=True, null=True)
    warranty = models.CharField(max_length=100, blank=True, null=True)
    problem = models.CharField(max_length=100, blank=True, null=True)
    received_date = models.DateField(blank=True,null=True)
    estimated_date = models.DateField(blank=True,null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(null=True, blank=True)
    referance_image = models.ImageField(null=True, blank=True)
    spare = models.CharField(max_length=100, blank=True, null=True)
    estimated_cost = models.CharField(max_length=100, blank=True, null=True)
    mail_status = models.CharField(max_length=100, blank=True, null=True, default=0)


    def __str__(self):
        return self.name

    class Meta:
        db_table = "customer"
        verbose_name = 'CUSTOMER'


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, first_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, first_name, password, role = "" ,  **other_fields)

    def create_user(self, email, user_name, first_name, password,role , **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          first_name=first_name,role=role, **other_fields)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user

class NewUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    mobile = models.CharField(max_length=120, blank=True)
    ROLES = (
        ('ADMIN', 'ADMIN'),
        ('STAFF', 'STAFF'),
    )
    role = models.CharField(_('User Role'), max_length=50, choices=ROLES)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name']

    def __str__(self):
        return self.user_name

    class Meta:
        db_table = "USERS"
        verbose_name = 'User'
