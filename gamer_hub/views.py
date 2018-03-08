from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from gamer_hub.models import Page, UserProfile
from gamer_hub.forms import UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from registration.backends.simple.views import RegistrationView

def index(request):
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'pages': page_list}

    response = render(request, 'gamer_hub/index.html', context_dict)
    return response

def logout(request):
    context_dict = {}
    response = render(request, 'registration/logout.html', context_dict)
    return response
	
@login_required
def register_profile(request):
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            return redirect('index')
        else:
            print(form.errors)

    context_dict = {'form': form}

    return render(request, 'gamer_hub/profile_registration.html', context_dict)


class gamer_hubRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return reverse('register_profile')
		
@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    uploads = Upload.objects.filter(user=user)
    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm(
        {'website': userprofile.website, 'picture': userprofile.picture, 'bio': userprofile.bio})

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile', user.username)
        else:
            print(form.errors)

    return render(request, 'gamer_hub/profile.html',
                  {'userprofile': userprofile, 'selecteduser': user, 'form': form, 'uploads': uploads})


def list_profiles(request):
    userprofile_list = UserProfile.objects.all()

    return render(request, 'gamer_hub/list_profiles.html',
                  {'userprofile_list': userprofile_list})