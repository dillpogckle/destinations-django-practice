from django.db import models


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    email = models.TextField(unique=True)
    password_hash = models.TextField()


class Session(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.TextField(unique=True)


class Destination(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    review = models.TextField()
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    share_publicly = models.BooleanField(default=False)
