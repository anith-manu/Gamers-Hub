from django.contrib import admin
from gamer_hub.models import UserProfile, Game, Review, Platform

admin.site.register(UserProfile)
admin.site.register(Game)
admin.site.register(Review)
admin.site.register(Platform)
