import os
import django
from gamer_hub.models import Platform, Game, Review, UserProfile
import sys
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from datetime import datetime
import dateutil.parser
from django.core.files.images import ImageFile
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'gamer_hub_project.settings')
django.setup()


def populate():
    users = [
        ('user_1', 'phgzHpXcnJ', 'user_1@example.com'),
        ('user_2', 'ktMmqKcpJw', 'user_2@example.com'),
    ]
    # platform is a list of string written exactly like the name of the platform in the platform list
    # url is the string of symbols copied from the end of the youtube video url
    # for the picture you have to download it, put it in media\game_covers and copy its name
    games = [
        {'title': 'Dark Sous 3', 'publisher': 'From Software', 'game_info': 'Play as undead etc..',
         'genre': 'Action-RPG', 'release_date': '24.03.2016', 'platforms': ['PC', 'PS4', 'Xbox One'],
         'url': '_zDZYrIUgKE', 'cover': '2760211-ds3_cover_art.png'}
    ]

    platforms = [
        {'name': 'PC'},
        {'name': 'PS4'},
        {'name': 'Xbox One'},
        {'name': 'PS3'},
        {'name': 'Xbox360'},
    ]

    add_users(users)
    for platform in platforms:
        add_platform(platform['name'])

    for game in games:
        add_game(game)


def add_users(users):
    for username, password, email in users:
        try:
            print ('Creating user {0}.'.format(username))
            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.save()

            assert authenticate(username=username, password=password)
            print ('User {0} successfully created.'.format(username))

        except:
            print ('There was a problem creating the user: {0}.  Error: {1}.' \
                .format(username, sys.exc_info()[1]))

    for user in User.objects.all():
        user_profile = UserProfile.objects.get_or_create(user=user)[0]


def add_platform(platform_name):
    p = Platform.objects.get_or_create(name=platform_name)[0]
    p.save()
    return p


def add_game(game):
    g = Game.objects.get_or_create(title=game['title'])[0]
    g.genre = game['genre']
    g.release_date = dateutil.parser.parse(game['release_date'])
    g.game_info = game['game_info']
    g.publisher = game['publisher']
    g.youtube_url = game['url']
    picture_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'game_covers')
    img_file = open(picture_path + "\\" + game['cover'], "rb")
    g.picture.save(game['title']+'png', img_file, save=True)
    for plat in game['platforms']:
        g.platform.add(Platform.objects.get_or_create(name=plat)[0])
    g.save()
    return g


if __name__ == '__main__':
    print("Starting Gamer Hub population script...")
    populate()
