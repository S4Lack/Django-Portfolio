from django.contrib import admin
from django.utils.text import slugify

from .models import *

# Register your models here.

class PostAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('title',)}

admin.site.register(Profile)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(PostComment)
# prepopulate the psot slug