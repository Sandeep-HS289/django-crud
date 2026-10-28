from django.db import models

# Create your models here.
class Students(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    branch = models.CharField(max_length=100)

    objects = models.Manager()

    def __str__(self) -> str:
        return self.name


