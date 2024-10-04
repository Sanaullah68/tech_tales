from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user  = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.CharField(max_length=233)
    address = models.CharField(max_length=233)
    profile_image = models.ImageField(blank=True,upload_to='User_images/')
    def __str__(self):
        return self.user.username

class Blog(models.Model):
    STATUS = (('submitted','submitted'),('pending','pending'),('verified','verified'),('rejected','rejected'))
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=233,unique= True)
    content = models.TextField()
    image = models.ImageField(blank=True,upload_to='blog_images/')
    blog_url = models.URLField(blank=True)
    video = models.CharField(max_length=122,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    feed_back_to_user = models.CharField(blank=True,max_length=200)
    status = models.CharField(blank=True,choices=STATUS,max_length=20,default='submitted')
    def __str__(self):
        return f"{self.title} by {self.user.username}"

class Contact(models.Model):
    name = models.CharField(max_length=233)
    email = models.EmailField()
    subject = models.CharField(max_length=233)
    message = models.TextField()

    def __str__(self):
        return self.name
    
class News(models.Model):
    STATUS = (('submitted','submitted'),('pending','pending'),('verified','verified'),('rejected','rejected'))
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=233,unique=True)
    content = models.TextField()
    image = models.ImageField(blank=True,upload_to='news_images/')
    news_url = models.URLField(blank=True)
    video = models.CharField(max_length=122,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True)
    is_verified = models.BooleanField(blank=True,default=False) 
    feed_back_to_user = models.CharField(blank=True,max_length=200)
    status = models.CharField(blank=True,choices=STATUS,max_length=20,default='submitted')
    def __str__(self):
        return f"{self.title} by {self.user.username}"
