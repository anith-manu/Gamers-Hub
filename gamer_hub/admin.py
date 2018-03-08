from django.contrib import admin
from gamer_hub.models import Category, Page, UserProfile

class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('name',)}

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

admin.site.register(Page, PageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(UserProfile)
