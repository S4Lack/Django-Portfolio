from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from .models import Post, PostComment, Profile
from .filters import PostFilter
from .forms import ProfileForm, UserForm

# Create your views here.
def index(request):
    posts = Post.objects.filter(active=True).order_by("-pk")[0:3]
    
    context = {"posts": posts}
    return render(request, "portfolio/index.html", context)


def post(request, slug):
    post = Post.objects.get(slug=slug)
    
    if request.method == "POST":
      PostComment.objects.create(
        author = request.user.profile, 
        post = post, 
        context = request.POST.get("comment", None)
      )
      messages.success(request, "Your comment was successfully added!")
      
      return redirect("post", slug=post.slug)
      
    context = {"post": post}
    return render(request, "portfolio/post.html", context)


def posts(request):
    posts = Post.objects.filter(active=True)
    postFilter = PostFilter(request.GET, queryset=posts)
    posts = postFilter.qs
    
    paginator = Paginator(posts, 9)
    page = request.GET.get("page")
    
    try:
      posts = paginator.page(page)
    except PageNotAnInteger:
      posts = paginator.page(1)
    except EmptyPage:
      posts = paginator.page(paginator.num_pages)
      
    context = {"posts": posts, "postFilter": postFilter}
    return render(request, "portfolio/posts.html", context)
  

# Auth Views
@login_required(login_url='home')  
def userAccount(request):
  profile = request.user.profile
  
  context = {"profile": profile}
  return render(request, "portfolio/account.html", context)


@login_required(login_url="home")
def updateProfile(request):
  user = request.user
  profile = user.profile
  form = ProfileForm(instance=profile)
  
  if request.method == "POST":
    # Update The Related User Instance
    user_form = UserForm(request.POST, instance=user)
    if user_form.is_valid():
      user_form.save()
  
    # Update The Profile Instance
    form = ProfileForm(request.POST, request.FILES, instance=profile)
    if form.is_valid():
      form.save()
      return redirect("account")
    
  context = {"form": form}
  return render(request, "portfolio/profile_form.html", context)    


