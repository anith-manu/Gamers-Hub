from django.conf.urls import url, include
from gamer_hub import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^register_profile/$', views.register_profile, name='register_profile'),
	url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
    url(r'^profiles/$', views.list_profiles, name='list_profiles'),
	url(r'^logout/$', views.logout, name='logout'),
]
