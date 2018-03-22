from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from gamer_hub.models import Page, UserProfile, Game, Review, Platform
from gamer_hub.forms import UserProfileForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from registration.backends.simple.views import RegistrationView
from django.http import HttpResponseRedirect, HttpResponse


def index(request):
    games_release_date_list = Game.objects.order_by('-release_date')[:3]
    games_rating_list = Game.objects.order_by('-rating')[:3]
    context_dict = {"games_release_date": games_release_date_list, "games_rating": games_rating_list}
    return render(request, 'gamer_hub/index.html', context_dict)


def logout(request):
    context_dict = {}
    response = render(request, 'registration/logout.html', context_dict)
    return response



class gamer_hubRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return reverse('register_profile')


@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm(
        {'mygames': userprofile.mygames, 'picture': userprofile.picture, 'bio': userprofile.bio})

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile', user.username)
        else:
            print(form.errors)

    context_dict = {'userprofile': userprofile, 'selecteduser': user, 'form': form}
    reviews = Review.objects.filter(user__user=user.id)
    top_reviews = get_top_reviews(reviews)
    games_highest_rated_reviews = [review.game_title for review in top_reviews]
    context_dict['top_reviews'] = get_top_reviews(reviews)
    context_dict['top_games'] = set(games_highest_rated_reviews)
    return render(request, 'gamer_hub/profile.html', context_dict)


def list_profiles(request):
    userprofile_list = UserProfile.objects.all()

    return render(request, 'gamer_hub/list_profiles.html',
                  {'userprofile_list': userprofile_list})


def modify_game_score(game_slug):
    """ Auxiliary function which modifies the score field
    in the game model based on the game's reviews"""
    reviews = Review.objects.filter(game_title__slug=game_slug)
    scores = [review.score for review in reviews]
    if len(scores) > 0:
        avg_rating = sum(scores)/len(scores)
    else:
        avg_rating = 0
    game = Game.objects.get(slug=game_slug)
    game.rating = avg_rating
    game.save()


def modify_all_games_score():
    """Auxiliary function which calls modify_game_score
    on all games"""
    games = Game.objects.all()
    for game in games:
        modify_game_score(game.slug)


def get_top_reviews(reviews, number_of_reviews=4):
    sorted_reviews = list(reviews)
    sorted_reviews.sort(key=lambda x: x.points, reverse=True)
    if len(sorted_reviews) >= number_of_reviews:
        sorted_reviews = sorted_reviews[:number_of_reviews]
    else:
        sorted_reviews = sorted_reviews[:len(sorted_reviews)]
    return sorted_reviews


def about_us(request):
    return render(request, 'gamer_hub/about_us.html')


def show_platform(request, platform_slug):
    games_release_date_list = Game.objects.filter(platform__slug=platform_slug).order_by('-release_date')[:100]
    games_rating_list = Game.objects.filter(platform__slug=platform_slug).order_by('-rating')[:100]
    context_dict = {"games_release_date": games_release_date_list, "games_rating": games_rating_list}
    platform = get_object_or_404(Platform, slug=platform_slug)
    context_dict['platform'] = platform
    return render(request, 'gamer_hub/show_platform.html', context_dict)


def show_genre(request, genre):
    games_release_date_list = Game.objects.filter(genre=genre).order_by('-release_date')[:100]
    games_rating_list = Game.objects.filter(genre=genre).order_by('-rating')[:100]
    context_dict = {"games_release_date": games_release_date_list, "games_rating": games_rating_list}
    context_dict['genre'] = genre
    return render(request, 'gamer_hub/show_genre.html', context_dict)


def delete_review(request, review_id):
    review = get_object_or_404(Review, review_id=review_id)
    game_title = review.game_title
    game = get_object_or_404(Game, title=game_title)
    review.delete()
    return HttpResponseRedirect(reverse("show_game", kwargs={'game_name_slug': game.slug}))


def vote(request):
    review_id = request.POST.get('review_id')
    vote_action = request.POST.get('action')
    vote_type = request.POST.get('type')
    review = get_object_or_404(Review, review_id=review_id)
    user_profile = get_object_or_404(UserProfile, user=request.user)
    reviews_upvoted = user_profile.reviews_upvoted.all()
    reviews_downvoted = user_profile.reviews_downvoted.all()
    if vote_action == 'vote':
        if vote_type == 'up':
            if review in reviews_downvoted:
                user_profile.reviews_downvoted.remove(review)
                user_profile.reviews_upvoted.add(review)
                review.points = review.points+2
            elif review not in reviews_downvoted and review not in reviews_upvoted:
                user_profile.reviews_upvoted.add(review)
                review.points += 1
            else:
                return HttpResponse('Error-cannot upvote an upvoted review')
        elif vote_type == 'down':
            if review in reviews_upvoted:
                user_profile.reviews_upvoted.remove(review)
                user_profile.reviews_downvoted.add(review)
                review.points = review.points-2
            elif review not in reviews_downvoted and review not in reviews_upvoted:
                user_profile.reviews_downvoted.add(review)
                review.points -= 1
            else:
                return HttpResponse('Error-cannot downvote a downvoted review')
        else:
            return HttpResponse('Error-unknown vote type')
    elif vote_action == 'recall-vote':
        if vote_type == 'up':
            user_profile.reviews_upvoted.remove(review)
            review.points = review.points-1
        elif vote_type == 'down':
            user_profile.reviews_downvoted.remove(review)
            review.points = review.points+1
        else:
            return HttpResponse('error - unknown vote type or no vote to recall')
    else:
        return HttpResponse('error - bad action')
    review.save()
    return HttpResponse(review.points)


def show_game(request, game_name_slug):
    modify_game_score(game_name_slug)
    context_dict = {}
    game = get_object_or_404(Game, slug=game_name_slug)
    reviews = Review.objects.filter(game_title__slug=game_name_slug)
    context_dict['game'] = game
    context_dict['avg_rating'] = game.rating
    context_dict['top_reviews'] = get_top_reviews(reviews, number_of_reviews=len(reviews))
    context_dict['reviews'] = reviews
    if request.user.is_authenticated():
        user_profile = UserProfile.objects.get(user=request.user)
        context_dict['reviews_upvoted'] = user_profile.reviews_upvoted.all()
        context_dict['reviews_downvoted'] = user_profile.reviews_downvoted.all()
        if request.method == 'POST':
            form = ReviewForm(request.POST, user_profile=user_profile, game_title=game)
            if form.is_valid():
                form.save(commit=True)
                return HttpResponseRedirect(reverse("show_game", kwargs={'game_name_slug': game_name_slug}))
            else:
                print(form.errors)
        else:
            form = ReviewForm(user_profile=user_profile, game_title=game)
        context_dict['form'] = form
    return render(request, 'gamer_hub/show_game.html', context_dict)


def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        all_games = Game.objects.all()
        games = []
        for game in all_games:
            if q.lower() in game.title.lower():
                games.append(game)
        return render(request, 'gamer_hub/search_result.html', {'games': games, 'query': q})
    else:
        return HttpResponse('search here')