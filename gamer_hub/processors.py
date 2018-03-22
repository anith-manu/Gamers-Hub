from gamer_hub.models import Game, Platform


def get_platforms_and_genres(request):
    platforms = Platform.objects.all()
    games = Game.objects.all()
    genres = [game.genre for game in games]
    genres = set(genres)
    return {'platforms': platforms, 'genres': genres}
