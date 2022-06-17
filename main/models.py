from datetime import datetime
from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    datetime = models.DateTimeField(default='')
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.email
