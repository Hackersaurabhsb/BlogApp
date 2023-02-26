from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.db.models import Count
from django.conf import settings
from django import forms
from django.conf import settings
#creting classes to show our models
class Post(models.Model):
    Status_choices=(
        ('draft','Draft'),
        ('published','Published'),
    )
    title=models.CharField(max_length=40)
    slug=models.SlugField(max_length=250,unique_for_date='publish',blank=True,null=False)
    author=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='blog_posts',on_delete=models.CASCADE)
    body=models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=10,choices=Status_choices,default='draft')
    class Meta:
        ordering=('-publish',)
    def __str__(self):
        return self.title
    tags=TaggableManager()
    def get_absolute_url(self):
        return "/post/%i/" % self.id
class comment(models.Model):
    post=models.ForeignKey(Post, related_name='comments',on_delete=models.CASCADE)
    name=models.CharField(max_length=80)
    email=models.EmailField()
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)
    class Meta:
        ordering=('-created',)
    def __str__(self):
        return 'Comment by {} on {}'.format(self.name,self.post)

class login(models.Model):
    username=models.CharField(max_length=30)
    password=models.CharField(max_length=30)


class Profile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo=models.ImageField(upload_to='users/%y/%m/%d/',blank=True,null=True)
    date_of_birth=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Profile of {self.user.username}'