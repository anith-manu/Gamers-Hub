from django.contrib import admin
from gamer_hub.models import Category, Page, UserProfile, Game, Review, Platform


class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('name',)}


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')


admin.site.register(Page, PageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(UserProfile)
admin.site.register(Game)
admin.site.register(Review)
admin.site.register(Platform)
