from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    service = models.CharField(max_length=100)
    message = models.CharField(max_length=3000)
    from_value = models.CharField(max_length=30)
    to_value = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}::{self.email}::{self.service}'

# Create your models here.
