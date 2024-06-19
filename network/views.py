from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User, Post


def index(request):
    all_posts = Post.objects.all().order_by('-date')
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "page_obj": page_obj
    })


def following(request):
    user = User(pk=request.user.id)
    following_users = user.following.all()
    all_posts = Post.objects.all().order_by('-date')
    following_posts = [
        post for post in all_posts if post.user in following_users]

    paginator = Paginator(following_posts, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "page_obj": page_obj
    })


@login_required(redirect_field_name="login")
def create_post(request):
    if request.method == 'GET':
        return render(request, 'network/create_post.html')

    elif request.method == 'POST':
        content = request.POST['content'].strip()

        if not content:
            return render(request, 'network/create_post.html', {
                'message': "Post text is empty!"
            })

        try:
            user = User.objects.get(pk=request.user.id)
            Post(content=content, user=user).save()
        except:
            return render(request, 'network/create_post.html', {
                'message': "Error!"
            })

        return HttpResponseRedirect(reverse(index))


def profile(request, profile_id):
    if request.method == 'GET':

        try:
            profile = User.objects.get(pk=profile_id)
        except:
            return HttpResponseRedirect(reverse('index'))

        # get posts of profile
        posts = Post.objects.filter(user=profile).order_by('-date')

        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        return render(request, "network/profile.html", {
            "page_obj": page_obj,
            "profile_data": profile
        })


@login_required(redirect_field_name='login')
def follow(request, user_id):
    if request.method == 'POST':
        # get user and profile data
        user = User.objects.get(pk=user_id)
        profile_id = request.POST['profile']
        profile = User.objects.get(pk=profile_id)

        # user follows profile
        user.following.add(profile)
        return HttpResponseRedirect(reverse('profile', args=[profile_id]))


@login_required(redirect_field_name='login')
def unfollow(request, user_id):
    if request.method == 'POST':
        # get user and profile data
        user = User.objects.get(id=user_id)
        profile_id = request.POST['profile']
        profile = User.objects.get(id=profile_id)

        # user unfollows profile
        user.following.remove(profile)
        return HttpResponseRedirect(reverse('profile', args=[profile_id]))


@csrf_exempt
def like(request, post_id):
    if request.method == 'PUT':
        data = json.load(request)
        user = User.objects.get(pk=int(data['user_id']))
        post = Post.objects.get(pk=post_id)
        if user in post.like.all():
            post.like.remove(user)
            return JsonResponse({
                'message': 'disliked',
                'likes': post.like.all().count()
            })
        else:
            post.like.add(user)
            return JsonResponse({
                'message': 'liked',
                'likes': post.like.all().count()
            })


@csrf_exempt
def edit(request, post_id):
    if request.method == 'PUT':
        post = Post.objects.get(pk=post_id)

        if request.user != post.user:
            return JsonResponse({
                'message': 'Unauthorised!'
            })

        data = json.load(request)
        post.content = data['content']
        post.save()

        return JsonResponse({
            'message': 'successfull',
            'content': post.content
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
