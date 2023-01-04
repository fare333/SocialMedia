from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.


@login_required(login_url="profiles:login")
def post_comment_create_list_view(request):
    qs = Post.objects.all()
    profile = Profile.objects.get(user=request.user)
    
    p_form = PostModelForm()
    c_form = CommentModelForm()
    post_added = False
    
    profile = Profile.objects.get(user=request.user)
    
    if "submit_p_form" in request.POST:
        p_form = PostModelForm(request.POST, request.FILES)
        if p_form.is_valid():
            obj = p_form.save(commit=False)
            obj.author = profile
            obj.save()
            p_form = PostModelForm()
            post_added = True
    
    if request.method == "POST":
        c_form = CommentModelForm(request.POST)
        if c_form.is_valid():
            obj = c_form.save(commit=False)
            obj.author = profile
            obj.post = Post.objects.get(id=request.POST.get("post_id"))
            obj.save()
            c_form = CommentModelForm()

    
    context = {
        'qs': qs,
        "profile":profile,
        "p_form":p_form,
        "c_form":c_form,
        "post_added":post_added,
    }
    return render(request, 'posts/main.html', context)
    
@login_required(login_url="profiles:login")
def like_unlike_post(request):
    user = request.user
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post_model = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)
        if profile in post_model.liked.all():
            post_model.liked.remove(profile)
        else:
            post_model.liked.add(profile)

        like,created = Like.objects.get_or_create(user=profile,post_id=post_id)
    
        if not created:
            if like.value == "Like":
                like.value = "Unlike"
            else:
                like.value ="Like"
                
        else:
            like.value = "Like"
            
            post_model.save()
            like.save()
            
        
        return redirect("posts:all")
        
@login_required(login_url="profiles:login")
def remove(request,pk):
    post = Post.objects.get(id=pk)
    if request.user == post.author.user:
        if request.method == "POST":
            post.delete()
            return redirect("posts:all")
    return render(request, 'posts/remove.html')

@login_required(login_url="profiles:login")
def update(request,pk):
    post = Post.objects.get(id=pk)
    form = PostModelForm(instance=post)
    if request.user == post.author.user:
        if request.method == "POST":
            form = PostModelForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return redirect("posts:all")
    else:
        return redirect("posts:all")
    
    context = {"form":form}
    return render(request, 'posts/update.html', context)

@login_required(login_url="profiles:login")
def search_method(request):
    if request.method == "POST":
        search = request.POST.get("search")
        profiles = Profile.objects.filter(Q(user__username__icontains=search)).exclude(user=request.user)
        
    context = {"profiles":profiles}
    return render(request, 'posts/search.html', context)