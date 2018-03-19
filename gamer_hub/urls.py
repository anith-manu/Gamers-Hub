from django.conf.urls import url, include
from gamer_hub import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^register_profile/$', views.register_profile, name='register_profile'),
	url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
    url(r'^profiles/$', views.list_profiles, name='list_profiles'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^game/(?P<game_name_slug>[\w\-]+)/$', views.show_game, name='show_game'),
    url(r'^genre/(?P<genre>[\w\-]+)/$', views.show_genre, name='show_genre'),
    url(r'^platform/(?P<platform_slug>[\w\-]+)/$', views.show_platform, name='show_platform'),
    url(r'^vote/$', views.vote, name='vote'),


]
