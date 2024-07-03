from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
 
 
class User(AbstractUser):
 
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
    city = models.CharField(max_length=50)
    interests = models.ManyToManyField('Interests', related_name='all_users')
    date = models.DateField()
    description = models.TextField(max_length=1500)
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

    class Meta:  
        verbose_name = 'Профиль'  
        verbose_name_plural = 'Профили'  

    # def save(self, *args, **kwargs):  
    #     if not self.user_avatar:  
    #         encoded_username = quote(self.user.username, safe='')
    #         image_url = f'https://robohash.org/{encoded_username}'  
    #         response = request.urlopen(image_url)  
    #         self.user_avatar.save(f'{self.user.username}.png', response, save=False)  
    #     super().save(*args, **kwargs)  

    #     img = Image.open(self.user_avatar.path)  

    #     if img.height > 300 or img.width > 300:  
    #         output_size = (300, 300)  
    #         img.thumbnail(output_size)  
    #         img.save(self.user_avatar.path)  

class Interests(models.Model):
    name = models.CharField(max_length=50)