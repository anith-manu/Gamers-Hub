from django import forms
from django.contrib.auth.models import User
from gamer_hub.models import UserProfile, Review, Game
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('mygames', 'bio', 'picture')


class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user_profile = kwargs.pop('user_profile')
        game = kwargs.pop('game_title')
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['user'].initial = user_profile
        self.fields['game_title'].initial = game

    def clean_score(self):
        data = self.cleaned_data['score']
        data = int(data)
        if data < 1 or data > 10:
            raise ValidationError('Invalid Score. Score must be between 1 and 10.')
        return data

    user = forms.ModelChoiceField(UserProfile.objects.all(), widget=forms.HiddenInput())
    game_title = forms.ModelChoiceField(Game.objects.all(), widget=forms.HiddenInput())
    content = forms.CharField(max_length=800, help_text="Enter your text", widget=forms.Textarea)
    CHOICES = (('1', '1'), ('2', '2',), ('2', '3'),
               ('4', '4', ), ('5', '5',), ('6', '6'),
               ('7', '7', ), ('8', '8',), ('9', '9'), ('10', '10'))
    score = forms.ChoiceField(choices=CHOICES)
    class Meta:
        model = Review
        exclude = ('review_id', 'review_rating', 'points')
