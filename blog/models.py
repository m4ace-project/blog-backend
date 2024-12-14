from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
from accounts.models import User
from userProfile.models import ContentCreatorProfile

# Create your models here.

class Category(models.Model):
     name = models.CharField(max_length=30)
     
     class Meta:
          verbose_name_plural = "Categories"
     def __str__(self):
        return self.name


class Post(models.Model):
    post_id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = RichTextField(blank=False, null=False)
    blog_pic = models.ImageField(upload_to='blog_pics', null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=False, blank=False)
    

#     def save(self, *args, **kwargs):
#          # Check if the post is being published for the first time
#          if self.is_published and self.published_at is None:
#               self.published_at = timezone.now()

#          elif not self.is_published:
#               self.published_at = None      # Clear published date if unpublished

#          super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
     comment_id = models.BigAutoField(primary_key=True)
     post = models.ForeignKey(Post, on_delete=models.CASCADE)
     author = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
     content = models.TextField()
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)

     def __str__(self):
          return f"Comment by {self.author.username} on {self.post.title}"
     

class Like(models.Model):
     id = models.BigAutoField(primary_key=True)
     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Likes")
     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="Likes")
     created_at = models.DateTimeField(auto_now_add=True)

     class Meta:
          unique_together = ('user', 'post')  # Ensure a user can like a post only once

     def __str__(self):
          return f"{self.user.email} liked {self.post.title}"
     
class ReaderCategory(models.Model):
     reader = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reader_categories")
     category = models.ForeignKey(Category, on_delete=models.CASCADE)
     author = models.ForeignKey(ContentCreatorProfile, on_delete=models.CASCADE, related_name="favourite_by_readers")

     def __str__(self):
          return f"Reader ID: {self.reader.id} - Category: {self.category.name} - Author: {self.author.name}"
