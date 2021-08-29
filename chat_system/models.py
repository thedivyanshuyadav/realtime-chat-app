from django.db import models
from django_resized import ResizedImageField
# Create your models here.

def upload_directory(instance,filename):
    ext = filename.split('.')[-1]
    return f'user_{instance.id}/profile_picture.'+ext

class User(models.Model):
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(max_length=100,unique=True)
    password = models.CharField(max_length=100)
    profile_pic = ResizedImageField(size=[500,500],upload_to=upload_directory,default='default.png')
    class Meta:
        verbose_name_plural = "User"

    def __str__(self): return self.username



class Message(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='%(class)s_sender_requests_created')
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='%(class)s_receiver_requests_created')
    content = models.CharField(max_length=5000)
    datetime = models.DateTimeField()

    class Meta:
        ordering = ['datetime']

    def __str__(self):return str(self.id)


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_user_requests_created')
    contact = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_contact_requests_created')
    favourite = models.BooleanField(default=False)
    class Meta:
        ordering = ['contact']

    def __str__(self): return self.user.username + '-' + self.contact.username

def story_upload_directory(instance,filename):
    return f'story/{instance.id}/{filename}'

class Story(models.Model):
    user = models.ForeignKey(User,unique=True,on_delete=models.CASCADE, related_name='%(class)s_user_requests_created')
    story = ResizedImageField(size=[700,700],upload_to=story_upload_directory)
    datetime = models.DateTimeField()

    def __str__(self): return self.user.username

