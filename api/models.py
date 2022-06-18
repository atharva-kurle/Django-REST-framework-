from django.db import models

# Create your models here.
class User(models.Model):
    email = models.EmailField()
    password = models.TextField()

    def __str__(self):
        return self.email


class Books(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name