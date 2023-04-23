from django.db import models


class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    numOfImplants = models.IntegerField()
    implant = models.CharField(max_length=100)
    feedback = models.TextField()
    image = models.ImageField()


class Image(models.Model):
    img = models.ImageField()
