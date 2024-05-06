from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from pytz import timezone

from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Profile(models.Model):
  user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100, null=True, blank=True)
  email = models.CharField(max_length=100)
  profile_pic = models.ImageField(upload_to='images/', null=True, blank=True, default='user-icon.svg')
  bio = models.TextField(null=True, blank=True)
  
  def __str__(self):
    name = str(self.first_name)
    if self.last_name:
      name += ' ' + str(self.last_name)
    return name
  
  
class Tag(models.Model):
  name = models.CharField(max_length=50)
  
  def __str__(self):
    return self.name
  

class Post(models.Model):
  title = models.CharField(max_length=100)
  headline = models.CharField(max_length=200, null=True, blank=True)
  thumbnail = models.ImageField(upload_to='images/', null=True, blank=True, default="images/placeholder.svg")
  context = RichTextUploadingField(null=True, blank=True)
  created = models.DateTimeField(auto_now_add=True)
  active = models.BooleanField(default=False)
  tags = models.ManyToManyField(Tag, null=True, blank=True)
  slug = models.SlugField(null=True, blank=True, db_index=True)
  
  def __str__(self):
    return self.title
  
  def save(self, *args, **kwargs):
    base_slug = slugify(self.title)
    
    if not self.pk:
      count = 1
      while Post.objects.filter(slug=base_slug).exists():
        count += 1
        base_slug = slugify(self.title) + "-" + str(count)
        
      self.slug = base_slug
    
    elif self.pk:
      if self.slug.startswith(base_slug):
        pass
      else:
        count = 1
        while Post.objects.filter(slug=base_slug).exists():
          count += 1
          base_slug = slugify(self.title) + "-" + str(count)
        
        self.slug = base_slug
    
    super().save(*args, **kwargs)
        
    
class PostComment(models.Model):
  author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
  post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)      
  context = models.TextField()
  created = models.DateTimeField(auto_now_add=True)  
  
  def __str__(self):
    return self.context
  
  #@property
  #def created_dynamic(self):
  #  return timezone.now()
  
  
