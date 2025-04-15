from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AvatarImage(models.Model):
    """Модель для хранения аватара пользователя"""
    src = models.ImageField(upload_to='app_user/avatars/',
                            default='app_user/avatars/default.png',
                            verbose_name='Ссылка'
                            )
    alt = models.CharField(max_length=255, verbose_name='Альтернативный текст')

    class Meta:
        verbose_name = 'Аватар'
        verbose_name_plural = 'Аватары'


class Profile(models.Model):
    """Модель профиля пользователя"""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile'
    )
    fullName = models.CharField(max_length=255, verbose_name='Полное имя')
    email = models.EmailField(verbose_name='E-mail',default='')
    phone = models.PositiveIntegerField(verbose_name='Телефон',
                                        blank=True,
                                        null=True,
                                        unique=True
                                        )
    balance = models.DecimalField(max_digits=10,
                                  decimal_places=2,
                                  verbose_name='Баланс',
                                  default=0
                                  )
    avatar = models.ForeignKey(
        AvatarImage,
        verbose_name='Аватар',
        related_name='profile',
        on_delete=models.CASCADE
    )