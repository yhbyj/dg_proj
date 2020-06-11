from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'old_boy_book'
        verbose_name = '书籍'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '《{}》'.format(self.title)


class User(models.Model):
    SEX_CHOICES = [
        (0, '男'),
        (1, '女'),
    ]
    name = models.CharField(max_length=64)
    pwd = models.CharField(max_length=32)
    phone = models.CharField(
        max_length=11,
        null=True,
        default=None
    )
    sex = models.IntegerField(choices=SEX_CHOICES, default=0)
    icon = models.ImageField(
        upload_to='icon',
        default='icon/default.jpg'
    )

    class Meta:
        db_table = 'old_boy_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}'.format(self.name)
