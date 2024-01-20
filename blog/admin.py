from django.contrib import admin
from blog.models import *

# Register your models here.

@admin.register(Post)

class PostModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'desc']

@admin.register(FeedBack)

class FeedBackAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email']