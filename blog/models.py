from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone


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
    media = models.JSONField(blank=True, null=True)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    

    def save(self, *args, **kwargs):
         # Check if the post is being published for the first time
         if self.is_published and self.published_at is None:
              self.published_at = timezone.now()

         elif not self.is_published:
              self.published_at = None      # Clear published date if unpublished

         super().save(*args, **kwargs)

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
     

class Reaction(models.Model):
     REACTION_TYPES = [
          ('like', 'Like'),
          ('love', 'Love'),
          ('laugh', 'Laugh'),
          ('angry', 'Angry'),
          ('sad', 'Sad'),
     ]

     user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
     post = models.ForeignKey('Post', related_name='reactions', on_delete=models.CASCADE)
     reaction_type = models.CharField(max_length=10, choices=REACTION_TYPES)
     created_at = models.DateTimeField(auto_now_add=True)

     class Meta:
          unique_together = ('user', 'post')      # Ensures each user can react only once per post

     def __str__(self):
          return f"{self.user} reacted {self.reaction_type} on {self.post}"