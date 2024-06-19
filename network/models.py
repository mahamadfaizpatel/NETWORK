from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField(
        'self', blank=True, symmetrical=False, related_name='followers')
    pass


class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posted_by')
    content = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User, related_name='liked', blank=True)

    def __str__(self):
        return f"'{self.content}' by {self.user} on {self.date.strftime(' %d %b %Y %H:%M:%S')}"
