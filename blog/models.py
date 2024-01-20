from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=150)
    desc = models.TextField()
    

class FeedBack(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    address = models.TextField(max_length=500, blank=True)
    msg = models.TextField(max_length=1000)
    def __str__(self):
        return self.name
    
    