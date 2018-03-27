import os, django, sys, uuid, dateutil.parser
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'gamer_hub_project.settings')
django.setup()
from gamer_hub.models import Platform, Game, Review, UserProfile
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from datetime import datetime
from django.core.files.images import ImageFile


def populate():
    users = [
        ('user_1', 'phgzHpXcnJ', 'user_1@example.com'),
        ('user_2', 'ktMmqKcpJw', 'user_2@example.com'),
    ]
    # platform is a list of string written exactly like the name of the platform in the platform list
    # url is the string of symbols copied from the end of the youtube video url
    # for the picture you have to download it, put it in media\game_covers and copy its name
    games = [
		{'title': 'Dark Souls 3', 'publisher': 'From Software', 'game_info': "Dark Souls III is an action role-playing game played in a third-person perspective, similar to previous games in the series. Throughout the game, players encounter different types of enemies, each with different behaviors. Some of them change their combat pattern during battles. The game places more focus on role-playing, in which the character builder is expanded and weapons are improved to provide more tactical options to players. The game features fewer overall maps than its predecessor Dark Souls II, but they are larger and more detailed, which encourages exploration.",
         'genre': 'Action-RPG', 'release_date': '24.03.2016', 'platforms': ['PC', 'PS4', 'Xbox One'], 'url': '_zDZYrIUgKE', 'cover': '2760211-ds3_cover_art.png'},
        {'title': 'Grand theft auto V', 'publisher': 'Rockstar Games', 'game_info': "Set within the fictional state of San Andreas, based on Southern California, the single-player story follows three criminals and their efforts to commit heists while under pressure from a government agency. The open world design lets players freely roam San Andreas open countryside and the fictional city of Los Santos, based on Los Angeles.",
         'genre': 'Action-Adventure', 'release_date': '18.11.2014', 'platforms': ['PC', 'PS4', 'Xbox One','PS3','Xbox360'], 'url': 'hvoD7ehZPcM', 'cover': 'Grand_Theft_Auto_V.png'},
		{'title': 'Overwatch', 'publisher': 'Blizzard Entertainment', 'game_info': 'Overwatch assigns players into two teams of six, with each player selecting from a roster of over 20 characters, known in-game as "heroes", each with a unique style of play, whose roles are divided into four general categories: Offense, Defense, Tank, and Support. Players on a team work together to secure and defend control points on a map or escort a payload across the map in a limited amount of time. ',
        'genre': 'FPS', 'release_date': '24.05.2017', 'platforms': ['PC', 'PS4', 'Xbox One'], 'url': 'FqnKB22pOC0', 'cover': 'overwatch-cover.jpg'},
		{'title': 'League of Legends', 'publisher': 'Riot Games', 'game_info': 'In League of Legends, players assume the role of an unseen "summoner" that controls a "champion" with unique abilities and battle against a team of other players or computer-controlled champions. The goal is usually to destroy the opposing teams "nexus", a structure which lies at the heart of a base protected by defensive structures, although other distinct game modes exist as well. Each League of Legends match is discrete, with all champions starting off fairly weak but increasing in strength by accumulating items and experience over the course of the game.[2] The champions and setting blend a variety of elements, including high fantasy, steampunk, and Lovecraftian horror.',
        'genre': 'MOBA', 'release_date': '27.10.2009', 'platforms': ['PC'], 'url': 'BGtROJeMPeE', 'cover': 'GameBox.jpg'},
		{'title': 'Forza Horizon 3', 'publisher': 'Microsoft Studios', 'game_info': 'Forza Horizon 3 is an open world racing video game developed by Playground Games and published by Microsoft Studios for Xbox One and Microsoft Windows 10. The game features cross-platform play between the two platforms.',
        'genre': 'Sports', 'release_date': '27.09.2016', 'platforms': ['PC','Xbox One'], 'url': 'RqkpT0qag5c', 'cover': '3079439-z.jpg'},
        {'title': "Dragon Age: Origins", 'publisher': "Electronic Arts", 'game_info': "Dragon Age: Origins is a role-playing game developed by BioWare and published by Electronic Arts. Set in the fictional kingdom of Ferelden during a period of civil strife, the game puts the player in the role of a warrior, mage, or rogue coming from an elven, human, or dwarven background. The player character is recruited into the Grey Wardens, an ancient order that stands against demonic forces known as 'Darkspawn', and is tasked with defeating the Archdemon that commands them and ending their invasion.",
        'genre': 'RPG', 'release_date': '3.11.2009', 'platforms': ['PC', 'Xbox360', 'PS3'], 'url': '4k81SFkhFG4', 'cover': '60232_front.jpg'},
        {'title': 'S.T.A.L.K.E.R.: Call of Pripyat', 'publisher': 'GSC World Publishing', 'game_info': "S.T.A.L.K.E.R.: Call of Pripyat is a first-person shooter survival horror video game. The game takes place in and around the city of Pripyat in Ukraine. The area is divided into three parts known as Zaton, Yanov, and the city of Pripyat itself. Each of these is a large playable area. The majority of Call of Pripyat's gameplay focuses on a combination of both post-apocalyptic horror, as well as tactical role-playing action, mostly revolving around the Chernobyl Nuclear Power Plant Exclusion Zone.",
         'genre': 'FPS', 'release_date': '2.10.2009', 'platforms': ['PC'], 'url': '_IiSD6yFLwg', 'cover': 'Stalker_Call_of_Pripyat_cover.jpg'},
        {'title': 'The Witcher 3: Wild Hunt', 'publisher': 'CD Projekt', 'game_info': "The Witcher 3: Wild Hunt is a 2015 action role-playing video game developed and published by CD Projekt. Played in an open world with a third-person perspective, players control protagonist Geralt of Rivia, a monster hunter known as a Witcher, who is looking for his missing adopted daughter on the run from the Wild Hunt: an otherworldly force determined to capture and use her powers. Players battle the game's many dangers with weapons and magic, interact with non-player characters, and complete main-story and side quests to acquire experience points and gold, which are used to increase Geralt's abilities and purchase equipment. Its central story has several endings, determined by the player's choices at certain points in the game.",
         'genre': 'RPG', 'release_date': '19.05.2015', 'platforms': ['PC', 'PS4', 'Xbox One'], 'url': 'c0i88t0Kacs', 'cover': 'image.jpg'},
    ]

    platforms = [
        {'name': 'PC'},
        {'name': 'PS4'},
        {'name': 'Xbox One'},
        {'name': 'PS3'},
        {'name': 'Xbox360'},
    ]

    reviews = [
        {'user': 'user_1', 'game_title': 'Dark Souls 3', 'score': 9, 'content': 'Almost perfect.'},
        {'user': 'user_1', 'game_title': 'The Witcher 3: Wild Hunt', 'score': 10, 'content': 'Best game ever.'}
    ]

    print('Adding users.')
    add_users(users)
    print()
    print('Adding platforms.')
    for platform in platforms:
        add_platform(platform['name'])
    print()
    print('Adding games.')
    for game in games:
        add_game(game)
    print()
    print('Adding reviews.')
    for review in reviews:
        add_review(review)
    print('Finished.')


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


def add_review(review):
    r = Review.objects.get_or_create(content=review['content'], user=UserProfile.objects.get_or_create(user=User.objects.get(username=review['user']))[0])[0]
    r.game_title = Game.objects.get_or_create(title=review['game_title'])[0]
    r.score = review['score']
    r.content = review['content']
    r.save()
    print(' Review added.')
    return r


def add_platform(platform_name):
    p = Platform.objects.get_or_create(name=platform_name)[0]
    p.save()
    print(' ' + platform_name + ' added.')
    return p


def add_game(game):
    g = Game.objects.get_or_create(title=game['title'])[0]
    g.genre = game['genre']
    g.release_date = dateutil.parser.parse(game['release_date'])
    g.game_info = game['game_info']
    g.publisher = game['publisher']
    g.youtube_url = game['url']
    picture_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'game_covers')
    # img_file = open(picture_path + "\\" + game['cover'], "rb")
    img_file = open(os.path.join(picture_path, game['cover']), "rb")
    g.picture.save(game['title']+'png', img_file, save=True)
    for plat in game['platforms']:
        g.platform.add(Platform.objects.get_or_create(name=plat)[0])
    g.save()
    print(' ' + game['title'] + ' added.')
    return g


if __name__ == '__main__':
    print("Starting Gamer Hub population script...")
    populate()
