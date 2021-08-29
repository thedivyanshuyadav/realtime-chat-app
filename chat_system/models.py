from django.db import models
from sorl.thumbnail import ImageField, get_thumbnail
# Create your models here.

def upload_directory(instance,filename):
    ext = filename.split('.')[-1]
    return f'user_{instance.id}/profile_picture.'+ext

class User(models.Model):
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(max_length=100,unique=True)
    password = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to=upload_directory,default='default.png')
    class Meta:
        verbose_name_plural = "User"

    def __str__(self): return self.username

    def save(self, *args, **kwargs):
        if self.profile_pic:
            self.profile_pic = get_thumbnail(self.profile_pic, '100x100', quality=75, format='JPEG')
        super(User, self).save(*args, **kwargs)


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
    story = models.ImageField(upload_to=story_upload_directory)
    datetime = models.DateTimeField()

    def __str__(self): return self.user.username


    def save(self, *args, **kwargs):
        if self.story:
            self.story = get_thumbnail(self.story, '150x150', quality=75, format='JPEG')
        super(Story, self).save(*args, **kwargs)
