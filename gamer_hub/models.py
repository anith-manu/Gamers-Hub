from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from random import randint

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__self(self):
        return self.name

    def __unicode__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title
		
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    mygames = models.CharField(blank=True, max_length=240)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    bio = models.CharField(blank=True, max_length=240)

    def __str__(self):
        return self.user.username

    def __unicode__(self):
        return self.user.username
		
class UserProfileForm(forms.ModelForm):
    mygames = forms.CharField(required=False)
    picture = forms.ImageField(required=False)
    bio = forms.CharField(required=False)

    class Meta:
        model = UserProfile
        exclude = ('user',)
