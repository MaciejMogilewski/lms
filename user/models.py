from django.db import models


class User(models.Model):
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    class Meta:
        verbose_name: "Custom User"
        verbose_name_plural: "Custom Users"

    def __str__(self):
        return self.login
