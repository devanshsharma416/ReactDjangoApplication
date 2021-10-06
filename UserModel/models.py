from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import MyUserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.signals import user_logged_in
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.

class NewUser(AbstractBaseUser, PermissionsMixin):
    username        = None
    email           = models.EmailField(unique=True, verbose_name='Email', blank=True, null=True)
    first_name      = models.CharField(max_length=200, blank= True)
    last_name       = models.CharField(max_length=200, blank= True)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    profile_pic     = models.ImageField(upload_to = "images/", null = True, blank = True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """ User full name"""
        first_name =self.first_name if self.first_name else ''
        last_name = self.last_name if self.last_name else ''
        return f"{first_name}{last_name}"

    def __str__(self):
        return self.email

class Article(models.Model):
    title          = models.CharField(max_length=100)
    description    = models.TextField(null=True, blank = True)
    slug           = models.SlugField(blank=True, null= True)
    is_public      = models.BooleanField(default=True)
    user           = models.ForeignKey(NewUser, on_delete=models.CASCADE, blank=True, null=True)
    summary        = models.CharField(max_length=200, null=True, blank= True)

    class Meta:
        
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.title

class Lesson(models.Model):
    title          = models.CharField(max_length=120)
    description    = models.TextField(null=True, blank=True)
    is_public      = models.BooleanField(default=True)
    slug           = models.SlugField(blank=True, unique=True)
    user           = models.ForeignKey(NewUser, on_delete=models.CASCADE, blank=True, null=True)
    summary        = models.CharField(max_length=200, null=True, blank= True)
    

    class Meta:
    
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'


    def __str__(self):
        return self.title

class Tutorial(models.Model):
    title           = models.CharField(max_length=120)
    description     = models.TextField(null=True, blank=True)
    slug            = models.SlugField(blank=True, unique=True)
    is_public       = models.BooleanField(default=True)
    author          = models.CharField(max_length=20)
    user            = models.ForeignKey(NewUser, on_delete=models.CASCADE, blank=True, null=True)
    

    class Meta:
        
        verbose_name = 'Tutorial'
        verbose_name_plural = 'Tutorials'


    def __str__(self):
        return self.title


class Chapter(models.Model):
    title       =     models.CharField(max_length=120)
    description =     models.TextField(null=True, blank=True)
    slug        =     models.SlugField(blank=True, unique=True)
    is_public   =     models.BooleanField(default=True)
    author      =     models.CharField(max_length=20)
    user        =     models.ForeignKey(NewUser, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        
        verbose_name = 'Chapter'
        verbose_name_plural = 'Chapters'

    def __str__(self):
        return self.title

class Book(models.Model):
    title           = models.CharField(max_length=120)
    description     = models.TextField(null=True, blank=True)
    isbn            = models.CharField(max_length=20)
    is_public       = models.BooleanField(default=True)
    author          = models.CharField(max_length=20)
    user            = models.ForeignKey(NewUser, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        
        verbose_name = 'Book'
        verbose_name_plural = 'Books'


    def __str__(self): 
        return self.title

@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


def update_last_login(sender, user, **kwargs):
    """
    A signal receiver which updates the last_login date for
    the user logging in.
    """
    user.last_login = timezone.now()
    user.save(update_fields=['last_login'])
user_logged_in.connect(update_last_login)