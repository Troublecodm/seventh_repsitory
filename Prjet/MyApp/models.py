from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, null=True,blank=True,on_delete=models.CASCADE)
    username = models.CharField(max_length=200,null=True,blank=True)
    phone = models.CharField(max_length=50,null=True,blank=True)
    email = models.EmailField(max_length=254,null=True,blank=True)
    image  = models.ImageField(default='profile_picture.png',null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username

class ToDoList(models.Model):
    post_by = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=250,null=True,blank=True)
    desc = models.TextField()
    iscompleted = models.BooleanField(default=False)
    date_posted = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    # def __str__(self):
    #     return self.post_by
    

