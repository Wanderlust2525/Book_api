from django.db import models
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField
from phonenumber_field.modelfields import PhoneNumberField


from account.manages import UserManager




class User(AbstractUser):
    CLIENT = 'client'
    AUTHOR ='author'
    ADMIN = 'admin'

    ROLE= (
        (CLIENT, 'Читатель'),
        (AUTHOR, 'Автор'),
        (ADMIN, 'Администратор')
    )


    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('-date_joined',)

    username = None
    avatar = ResizedImageField('аватарка', size=[500, 500], crop=['middle', 'center'],
                               upload_to='avatars/', force_format='WEBP', quality=90,
                               null=True, blank=True)
    email = models.EmailField('электронная почта', blank=True, unique=True)
    role = models.CharField('роль', choices=ROLE, default=CLIENT, max_length=15)


    objects = UserManager()



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']


    @property
    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'
    get_full_name.fget.short_description = 'полное имя'
    def __str__(self):
        return f'{self.get_full_name}'

    

# Create your models here.
