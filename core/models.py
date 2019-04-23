from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Categories(models.Model):
    name = models.CharField(max_length=500, unique=True)
    product_count = models.IntegerField(default=0)
    url = models.URLField()
    off_id = models.TextField()


class Food(models.Model):
    name = models.CharField(max_length=500, unique=True)
    brand = models.CharField(max_length=250)
    nutriscore = models.CharField(max_length=1)
    fat = models.FloatField(null=True)
    saturated_fat = models.FloatField(null=True)
    sugars = models.FloatField(null=True)
    salt = models.FloatField(null=True)
    url = models.URLField(unique=True)
    image_url = models.URLField(unique=True,
                                default="https://upload.wikimedia.org/wikipedia/commons/c/c5/Foods.jpg")
    categories = models.ManyToManyField('Categories')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_foods = models.ManyToManyField(Food)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
