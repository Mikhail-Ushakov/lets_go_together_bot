from django.db import models
from django.contrib.auth.models import AbstractUser
 
 
class User(AbstractUser):
 
    class Genders(models.TextChoices):  
        UNDEFINED = 'U', 'не выбран'  
        MALE = 'M', 'мужской'  
        FEMALE = 'F', 'женский' 


    user_id = models.BigIntegerField(unique=True, primary_key=True)
    first_name = models.CharField(verbose_name="first name", max_length=150, blank=True)

    gender = models.CharField(max_length=1,  
                              choices=Genders.choices,  
                              default=Genders.UNDEFINED,  
                              verbose_name='Пол')  
    dob = models.IntegerField(blank=True,  
                           null=True,  
                           verbose_name='Возраст')  
    user_avatar = models.ImageField(upload_to='user/avatars/',  
                                    blank=True,  
                                    null=True,  
                                    verbose_name='Аватар пользователя')  
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




