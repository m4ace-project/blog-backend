from django.contrib import admin
from .models import ContentCreatorProfile, ReaderProfile


admin.site.register(ContentCreatorProfile)
admin.site.register(ReaderProfile)
