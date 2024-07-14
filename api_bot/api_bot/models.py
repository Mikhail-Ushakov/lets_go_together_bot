from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings
from .managers import CustomUserManager
 
class User(AbstractBaseUser, PermissionsMixin):
 
    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Genders(models.TextChoices):  
        UNDEFINED = 'U', 'не выбран'  
        MALE = 'M', 'мужской'  
        FEMALE = 'F', 'женский' 


    user_id = models.BigIntegerField(unique=True, primary_key=True)
    password = models.CharField("password", max_length=128, blank=True, null=True)

    name = models.CharField(verbose_name="first name", max_length=150, blank=True)

    gender = models.CharField(max_length=1,  
                              choices=Genders.choices,  
                              default=Genders.UNDEFINED,  
                              verbose_name='Пол')  
    age = models.IntegerField(blank=True,  
                           null=True,  
                           verbose_name='Возраст')  
    city = models.CharField(max_length=50, blank=True, null=True)
    interests = models.ManyToManyField('Interests', related_name='all_users')
    date = models.DateField(blank=True, null=True)
    description = models.TextField(max_length=1500, blank=True, null=True)
    user_avatar = models.CharField(max_length=150,
                                    blank=True,  
                                    null=True,  
                                    verbose_name='Аватар пользователя')  
    
    liked = models.ManyToManyField('self', symmetrical=False)
    not_liked = models.ManyToManyField('self', symmetrical=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        verbose_name="staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(default=True)
    class Meta:  
        verbose_name = 'Профиль'  
        verbose_name_plural = 'Профили'  


    def __str__(self) -> str:
        return self.name

class Interests(models.Model):
    name = models.CharField(max_length=50, unique=True)