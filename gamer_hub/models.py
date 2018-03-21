from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from random import randint
import uuid


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


class Platform(models.Model):
    name = models.CharField(unique=True, max_length=200)
    slug = models.SlugField(blank=True, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Platform, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Game(models.Model):
    title = models.CharField(unique=True, max_length=200)
    picture = models.ImageField(upload_to='game_covers', blank=True)
    game_info = models.CharField(max_length=500, blank=True)
    publisher = models.CharField(max_length=50, blank=True)
    platform = models.ManyToManyField(Platform)
    genre = models.CharField(max_length=200)
    release_date = models.DateField(null=True)
    slug = models.SlugField(blank=True, unique=True)
    rating = models.DecimalField(blank=True, default=1, decimal_places=2, max_digits=4)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Game, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Review(models.Model):
    review_id = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    content = models.CharField(max_length=800)
    user = models.ForeignKey('UserProfile')
    game_title = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True)
    score = models.IntegerField(default=1, blank=True)
    points = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.review_id


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    mygames = models.CharField(blank=True, max_length=240)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    bio = models.CharField(blank=True, max_length=240)
    reviews_upvoted = models.ManyToManyField(Review, blank=True, related_name='users_upvoted')
    reviews_downvoted = models.ManyToManyField(Review, blank=True, related_name='users_downvoted')

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
