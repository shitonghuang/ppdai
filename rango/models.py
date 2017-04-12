from __future__ import unicode_literals

from django.db import models

from django.template.defaultfilters import slugify

from django.contrib.auth.models import User

from django.utils import timezone

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    
    slug = models.CharField(max_length=128, unique=True)
    '''
    def save(self, *args, **kwargs):
                self.slug = self.name
                super(Category, self).save(*args, **kwargs)
    '''

    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128,default=None)
    time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(default=timezone.now)
    url = models.CharField(max_length=128,default=None)
    contents = models.CharField(max_length=600,default=None)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    sourcefile = models.FileField(upload_to='profile_file')

    def __unicode__(self):      #For Python 2, use __str__ on Python 3
        return self.title

class Loan(models.Model):
    #category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    amount = models.IntegerField(default=0)
    creditcode = models.IntegerField(default=0)
    listingid = models.IntegerField(default=0)
    months = models.IntegerField(default=0)
    payway = models.IntegerField(default=0)
    rate = models.IntegerField(default=0)

    def __unicode__(self):      #For Python 2, use __str__ on Python 3
        return self.title

class Product(models.Model):
    #category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    amount = models.IntegerField(default=0)
    rate = models.IntegerField(default=0)
    charge = models.IntegerField(default=0)

    def __unicode__(self):      #For Python 2, use __str__ on Python 3
        return self.title


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username





#3-22

class Comment(models.Model):
    page = models.ForeignKey(Page)
    author = models.CharField(max_length=128,default=None)
    time = models.DateTimeField(default=timezone.now)
    contents = models.CharField(max_length=600,default=None)
    dislikes = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    def __unicode__(self):      #For Python 2, use __str__ on Python 3
        return self.title


#3-22
class Notice(models.Model):
    
    title = models.CharField(max_length=128)
    
    time = models.DateTimeField(default=timezone.now)
    
    contents = models.CharField(max_length=600,default=None)
    
    def __unicode__(self):      #For Python 2, use __str__ on Python 3
        return self.title