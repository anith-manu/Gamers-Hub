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
        {'title': "Dragon Age: Origins", 'publisher': "Electronic Arts", 'game_info': 'Dragon Age: Origins is a role-playing game developed by BioWare and published by Electronic Arts. Set in the fictional kingdom of Ferelden during a period of civil strife, the game puts the player in the role of a warrior, mage, or rogue coming from an elven, human, or dwarven background. The player character is recruited into the Grey Wardens, an ancient order that stands against demonic forces known as Darkspawn, and is tasked with defeating the Archdemon that commands them and ending their invasion.',
         'genre': 'RPG', 'release_date': '3.11.2009', 'platforms': ['PC', 'Xbox360', 'PS3'], 'url': '4k81SFkhFG4', 'cover': '60232_front.jpg'},
        {'title': 'S.T.A.L.K.E.R.: Call of Pripyat', 'publisher': 'GSC World Publishing', 'game_info': 'S.T.A.L.K.E.R.: Call of Pripyat is a first-person shooter survival horror video game. The game takes place in and around the city of Pripyat in Ukraine. The area is divided into three parts known as Zaton, Yanov, and the city of Pripyat itself. Each of these is a large playable area. The majority of Call of Pripyats gameplay focuses on a combination of both post-apocalyptic horror, as well as tactical role-playing action, mostly revolving around the Chernobyl Nuclear Power Plant Exclusion Zone.',
         'genre': 'FPS', 'release_date': '2.10.2009', 'platforms': ['PC'], 'url': '_IiSD6yFLwg', 'cover': 'Stalker_Call_of_Pripyat_cover.jpg'},
        {'title': 'The Witcher 3: Wild Hunt', 'publisher': 'CD Projekt', 'game_info': 'The Witcher 3: Wild Hunt is a 2015 action role-playing video game developed and published by CD Projekt. Played in an open world with a third-person perspective, players control protagonist Geralt of Rivia, a monster hunter known as a Witcher, who is looking for his missing adopted daughter on the run from the Wild Hunt: an otherworldly force determined to capture and use her powers. Players battle the games many dangers with weapons and magic, interact with non-player characters, and complete main-story and side quests to acquire experience points and gold, which are used to increase Geralts abilities and purchase equipment. Its central story has several endings, determined by the players choices at certain points in the game.',
         'genre': 'RPG', 'release_date': '19.05.2015', 'platforms': ['PC', 'PS4', 'Xbox One'], 'url': 'c0i88t0Kacs', 'cover': 'image.jpg'},
        {'title': 'Fifa 18', 'publisher': 'EA', 'game_info': 'FIFA 18 is a sports game that simulates association football. The game features 52 fully licensed stadiums from 12 countries, including new stadiums, plus 30 generic fields equals to a total of 82.',
         'genre': 'Sports', 'release_date': '29.09.2017', 'platforms': ['PC', 'PS4', 'Xbox One','Xbox360','PS3'], 'url': 'z_7Gz_RFLnE', 'cover': 'FIFA 18.jpg'},
        {'title': 'Fortnite', 'publisher': 'Epic Games', 'game_info': 'One day, 98% of Earths population suddenly disappeared, and the remaining population found the skies covered in dense clouds, creating chaotic storms that dropped husks, humanoid zombie-like creatures, that attacked the living. The survivors found ways to construct storm shields, a field that cleared the storm clouds from immediately overhead and reduced the attacks from husks, and used these to set up survivor bases across the globe. The player is a commander of one of these bases, charged with going out of the storm shield to find resources, survivors, and other allies to help expand their storm shield and find a way to return Earth to its normal state.',
         'genre': 'Survival', 'release_date': '25.07.2017', 'platforms': ['PC', 'PS4', 'Xbox One'], 'url': 'xlaOaHvabH0', 'cover': 'fortnite-key-pve-salve-o-mundo-pacote-fundado-padro-D_NQ_NP_847879-MLB26919504864_022018-F.jpg'},
        {'title': 'Call of Duty: WWII', 'publisher': 'Activision', 'game_info': 'Similar to its predecessors, Call of Duty: WWII is a first-person shooter game. It removes the advanced system of movement present in the two previous Call of Duty titles, which included double jumping and wall running. Instead, it features a return of traditional movement to the series, taking it back to a "boots on the ground"[clarification needed] gameplay style. The game does not feature an unlimited sprint mechanic, seen in the previous two titles.[2] Instead of a "slide" movement mechanic, which allowed players to slide quickly on the ground, WWII features a "hit-the-deck" mechanic that allows the player to leap forward and throw themselves on the ground in order to get to cover quickly, similarly to a previous mechanic known as "dolphin dive" in Treyarchs Call of Duty: Black Ops and Call of Duty: Black Ops II.',
         'genre': 'FPS', 'release_date': '03.11.2017', 'platforms': ['PC', 'PS4', 'Xbox One'], 'url': 'D4Q_XYVescc', 'cover': 'cod.jpg'},
         {'title': 'Need for Speed Payback', 'publisher': 'Ghost Games', 'game_info': "Need for Speed Payback is a racing game set in an open world environment of Fortune Valley. It is focused on action driving and has three playable characters (each with different sets of skills) working together to pull off action movie like sequences. In contrast with the previous game, it also features a 24-hour day-night cycle. Unlike the 2015 Need for Speed reboot, Payback includes an offline single-player mode.",
          'genre': 'Sports', 'release_date': '10.06.2017', 'platforms': ['PC', 'PS4', 'Xbox One'], 'url': 'K-5EdHZ0hBs', 'cover': 'nfs.jpg'},
         {'title': 'Batman: Arkham City', 'publisher': 'Warner Bros.', 'game_info': "Batman: Arkham City is a 2011 action-adventure video game developed by Rocksteady Studios and published by Warner Bros. Interactive Entertainment. Based on the DC Comics superhero Batman, it is the sequel to the 2009 video game Batman: Arkham Asylum and the second installment in the Batman: Arkham series. Written by veteran Batman writer Paul Dini with Paul Crocker and Sefton Hill, Arkham City is inspired by the long-running comic book mythos. In the game's main storyline, Batman is incarcerated in Arkham City, a huge new super-prison enclosing the decaying urban slums of fictional Gotham City. He must uncover the secret behind the sinister scheme, Protocol 10, orchestrated by the facility's warden, Hugo Strange.",
          'genre': 'Action-Adventure', 'release_date': '18.10.2011', 'platforms': ['PC', 'PS4', 'Xbox One', 'PS3'], 'url': 'muCtJsy-d9w', 'cover': 'batman.jpg'},
         {'title': 'Red Dead Redemption', 'publisher': 'Rockstar Games', 'game_info': "The game is played from a third-person perspective in an open world environment, allowing the player to interact with the game world at their leisure. The player can travel the virtual world, a fictionalized version of the Western United States and Mexico, primarily by horseback and on foot. Gunfights emphasize a gunslinger gameplay mechanic called Dead Eye that allows players to mark multiple shooting targets on enemies in slow motion. The game makes use of a morality system, by which the player's actions in the game affect their character's levels of honor and fame and how other characters respond to the player. ",
          'genre': 'Action-Adventure', 'release_date': '18.05.2010', 'platforms': ['PS3', 'Xbox360'], 'url': '3gBctl1h_2o', 'cover': 'rdr.jpg'},
         {'title': 'Minecraft', 'publisher': 'Mojang', 'game_info': "Minecraft is a sandbox video game created and designed by Swedish game designer Markus Notch Persson, and later fully developed and published by Mojang. The creative and building aspects of Minecraft allow players to build with a variety of different cubes in a 3D procedurally generated world. Other activities in the game include exploration, resource gathering, crafting, and combat.",
          'genre': 'Adventure', 'release_date': '18.11.2011', 'platforms': ['PC'], 'url': 'MmB9b5njVbA', 'cover': 'minecraft.jpg'},
         {'title': 'The Elder Scrolls V: Skyrim', 'publisher': 'Bethesda Game Studios', 'game_info': "The game's main story revolves around the player character and their quest to defeat Alduin the World-Eater, a dragon who is prophesied to destroy the world. The game is set two hundred years after the events of Oblivion, and takes place in the fictional province of Skyrim. Over the course of the game, the player completes quests and develops the character by improving skills. The game continues the open world tradition of its predecessors by allowing the player to travel anywhere in the game world at any time, and to ignore or postpone the main storyline indefinitely.",
          'genre': 'Action-Adventure', 'release_date': '11.11.2011', 'platforms': ['PC', 'PS3', 'Xbox360'], 'url': 'JSRtYpNRoN0', 'cover': 'skyrim.jpg'},
         {'title': 'Fallout 4', 'publisher': 'Bethesda Game Studios', 'game_info': "The player assumes control of a character referred to as the Sole Survivor, who emerges from a long-term cryogenic stasis in Vault 111, an underground nuclear fallout shelter. After witnessing the murder of their spouse and kidnapping of their son, the Sole Survivor ventures out into the Commonwealth to search for their missing child. The player will subsequently explore the game's dilapidated world, complete various quests, help out factions, and acquire experience points to level up and increase the abilities of their character. New features to the series include the ability to develop and manage settlements, and an extensive crafting system where materials scavenged from the environment can be used to craft drugs and explosives, upgrade weapons and armor, and construct, furnish and improve settlements. Fallout 4 also marks the first game in the series to feature full voice acting for the protagonist.",
          'genre': 'Action-Adventure', 'release_date': '10.11.2015', 'platforms': ['PC', 'PS4', 'Xbox One'], 'url': 'GE2BkLqMef4', 'cover': 'fallout.jpg'},
         {'title': 'Naruto Shippuden', 'publisher': 'CyberConnect2', 'game_info': "The game features a revamped fighting system. It includes new ways of forming teams based on their skills as well as counterattacks and guard breaks. Masashi Kishimoto worked in the game by providing the new character Mecha-Naruto as well as new designs for the characters belonging to the organization Akatsuki whose back-stories are being told in this game. The game also includes a tournament mode where the player can battle against three CPU fighters at the same time, in an all-out battle royale format. Players are also able to customize characters.",
          'genre': 'Action-RPG', 'release_date': '11.09.2014', 'platforms': ['PC', 'PS3', 'Xbox360'], 'url': '1NKBruhXn-8', 'cover': 'naruto.jpg'},
         {'title': 'Rocket League', 'publisher': 'Psyonix', 'game_info': "Rocket League is a vehicular soccer video game developed and published by Psyonix. The game was first released for Microsoft Windows and PlayStation 4 in July 2015, with ports for Xbox One, macOS, Linux, and Nintendo Switch being released later on. In June 2016, 505 Games began distributing a physical retail version for PlayStation 4 and Xbox One, with Warner Bros. Interactive Entertainment taking over those duties by the end of 2017.",
          'genre': 'Sports', 'release_date': '17.02.2016', 'platforms': ['PC', 'PS4', 'Xbox One'], 'url': 'Vawwy2eu5sA', 'cover': 'rocket.jpg'},
         {'title': 'NBA 2K18', 'publisher': '2K Games', 'game_info': "NBA 2K18, like the previous games in the series, is based on the sport of basketball; more specifically, it simulates the experience of the National Basketball Association (NBA). Several game modes are present, including the team-managing MyGM and MyLeague modes, which were a considerable emphasis during development, and MyCareer, in which the player creates and plays through the career of their own player. The game features a licensed soundtrack consisting of 49 songs.",
          'genre': 'Sports', 'release_date': '19.09.2017', 'platforms': ['PC', 'PS4', 'PS3', 'Xbox One', 'Xbox360'], 'url': 'lwBqitrE3ww', 'cover': 'nba.jpg'},
         {'title': 'Tekken 7', 'publisher': 'Namco System ES3', 'game_info': "Tekken 7 is a fighting game developed and published by Bandai Namco Entertainment. The game is the ninth installment in the Tekken series, and the first to make use of the Unreal Engine. Tekken 7 had a limited arcade release in Japan in March 2015. An updated arcade version, Tekken 7: Fated Retribution, was released in Japan in July 2016, and features expanded content including new stages, costumes, items and characters. The same version was released for Microsoft Windows, PlayStation 4 and Xbox One in June 2017.",
          'genre': 'Action', 'release_date': '02.06.2017', 'platforms': ['PC', 'PS4', 'Xbox One'], 'url': 'tT_WsxCjprY', 'cover': 'tekken.jpg'},
         {'title': 'Far Cry 4', 'publisher': 'Ubisoft', 'game_info': "The game takes place in Kyrat, a fictional Himalayan country. The main story follows Ajay Ghale, a young Kyrati-American, as he is caught in a civil war involving Kyrat's Royal Army, controlled by tyrannical king Pagan Min, and a rebel movement called the Golden Path. Gameplay focuses on combat and exploration; players battle enemy soldiers and dangerous wildlife using a wide array of weapons. The game features many elements found in role-playing games, such as a branching storyline, and side quests. The game also features a map editor, a co-operative multiplayer mode, and an asymmetrical competitive multiplayer mode.",
          'genre': 'FPS', 'release_date': '18.11.2014', 'platforms': ['PC', 'PS4', 'PS3', 'Xbox360', 'Xbox One'], 'url': '6d60v1OErEY', 'cover': 'cry.jpg'},
         {'title': 'Madden NFL 18', 'publisher': 'Electronic Arts', 'game_info': "Madden NFL 18 is an American football sports video game based on the National Football League, developed and published by EA Sports for PlayStation 4 and Xbox One. The 29th installment of the Madden NFL series, the game features New England Patriots quarterback Tom Brady on the cover, the second straight year a Patriots player has the distinction, following tight end Rob Gronkowski.",
          'genre': 'Sports', 'release_date': '25.08.2017', 'platforms': ['PS4', 'Xbox One'], 'url': '8tvT0dgyV34', 'cover': 'madden.jpg'},
         {'title': 'Resident Evil 7', 'publisher': 'Capcom', 'game_info': "Resident Evil 7: Biohazard is a survival horror game developed and published by Capcom, released in January 2017 for Windows, PlayStation 4, and Xbox One. Following the more action-oriented Resident Evil 5 and Resident Evil 6, Resident Evil 7 returns to the franchise's survival horror roots, emphasizing exploration. The player controls Ethan Winters as he searches for his wife in a derelict plantation occupied by the cannibal Baker family, solving puzzles and fighting enemies. It is the first main Resident Evil game to use a first-person perspective.",
          'genre': 'Survival', 'release_date': '24.01.2017', 'platforms': ['PC', 'PS4', 'Xbox One'], 'url': 'W1OUs3HwIuo', 'cover': 're7.jpg'},
         {'title': 'Outlast 2', 'publisher': 'Unreal Engine', 'game_info': "Outlast 2 is a first-person survival horror video game developed and published by Red Barrels. It is the sequel to the 2013 video game Outlast, and features a journalist named Blake Langermann, along with his wife Lynn, roaming the Arizona desert to explore the murder of a pregnant woman only known as Jane Doe. Blake and Lynn get separated in a helicopter crash, and Blake has to find his wife while traveling through a village inhabited by a sect that believes the end of days are upon them.",
          'genre': 'Survival', 'release_date': '25.04.2017', 'platforms': ['PC', 'PS4', 'Xbox One'], 'url': 'EOrTuPljfPU', 'cover': 'outlast.jpg'},
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
        {'user': 'user_1', 'game_title': 'The Witcher 3: Wild Hunt', 'score': 10, 'content': 'Best game ever.'},
        {'user': 'user_2', 'game_title': 'The Witcher 3: Wild Hunt', 'score': 9, 'content': 'Best game ever.'}
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
    picture_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media', 'game_covers_src')
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
