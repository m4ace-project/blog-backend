from django.db import models

class ContentCreatorProfile(models.Model):
    profile_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('accounts.user', on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    name = models.CharField(max_length=255)
    bio =models.TextField()
    niches = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - Content Creator Profile"
    