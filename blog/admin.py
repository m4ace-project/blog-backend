from django.contrib import admin
from blog.models import Post, Category, Comment, Like

# Register your models here.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Like)