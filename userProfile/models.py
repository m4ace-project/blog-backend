from django.db import models

class ContentCreatorProfile(models.Model):
    profile_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('accounts.user', on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField()    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - Content Creator Profile"
    
class ReaderProfile(models.Model):
    reader_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('accounts.user', on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    bio = models.TextField()    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - Reader Profile"