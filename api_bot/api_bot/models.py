from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.conf import settings
from .managers import CustomUserManager
 
class User(AbstractBaseUser):
 
    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Genders(models.TextChoices):  
        UNDEFINED = 'U', 'не выбран'  
        MALE = 'M', 'мужской'  
        FEMALE = 'F', 'женский' 


    user_id = models.BigIntegerField(unique=True, primary_key=True)
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
    user_avatar = models.ImageField(upload_to='user/avatars/',  
                                    blank=True,  
                                    null=True,  
                                    verbose_name='Аватар пользователя')  
    
    liked = models.ManyToManyField('self', symmetrical=False)
    not_liked = models.ManyToManyField('self', symmetrical=True)
    is_staff = models.BooleanField(
        verbose_name="staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(default=True)
    class Meta:  
        verbose_name = 'Профиль'  
        verbose_name_plural = 'Профили'  

class Interests(models.Model):
    name = models.CharField(max_length=50)