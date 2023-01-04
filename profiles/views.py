from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from posts.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout

# Create your views here.
@login_required(login_url="profiles:login")
def my_profile(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(instance=profile)
    confirm = False
    if request.method == "POST":
        form = ProfileModelForm(request.POST or None,request.FILES or None,instance=profile)
        if form.is_valid():
            form.save()
            confirm = True
    context = {'profile': profile,"form":form,"confirm":confirm}
    return render(request, 'profiles/myprofile.html', context)

@login_required(login_url="profiles:login")
def invites_received_views(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invatations_received(profile)
    context = {'qs': qs}
    return render(request, 'profiles/invites_received.html', context)

@login_required(login_url="profiles:login")
def accept_invitation(request):
    if request.method=="POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.filter(pk=pk).first()
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect("profiles:my_invites")

@login_required(login_url="profiles:login")
def reject_invitation(request):
    if request.method=="POST":
        pk = request.POST.get("profile_pk")
        receiver = Profile.objects.get(user=request.user)
        sender = Profile.objects.filter(pk=pk).first()
        rel = Relationship.objects.filter(sender=sender, receiver=receiver).first()
        rel.delete()
    return redirect("profiles:my_invites")
        
@login_required(login_url="profiles:login")
def invite_profile_list_views(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)
    context = {'qs': qs}
    return render(request, 'profiles/invite_profile_list.html', context)

class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    # context_object_name = 'qs'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context

@login_required(login_url="profiles:login")
def get_profile_detail(request,slug):
    profile = Profile.objects.get(slug=slug)
    posts = Post.objects.filter(author=profile)
    context = {"profile":profile,"posts":posts}
    return render(request, 'profiles/profile_detail.html', context)


@login_required(login_url="profiles:login")
def sent_invitation(request):
    if request.method == "POST":
        pk = request.POST.get("profile_pk")
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)
        
        rel = Relationship.objects.create(sender=sender,receiver=receiver,status="send")
        
        return redirect('profiles:profile_list')
    
@login_required(login_url="profiles:login")
def remove_from_friend(request):
    if request.method == "POST":
        pk = request.POST.get("profile_pk")
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)
        
        rel = Relationship.objects.filter((Q(sender=sender) & Q(receiver=receiver) | Q(sender=receiver) & Q(receiver=sender)))
        
        rel.delete()
        
        return redirect('profiles:profile_list')    
    
def sign_in(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('posts:all')
        return render(request,'profiles/sign_in.html')
    return render(request,'profiles/sign_in.html')

@login_required(login_url="profiles:login")
def sign_out(request):
    logout(request)
    return redirect('profiles:login')

def register(request):
    form = Register()
    if request.method == "POST":
        form = Register(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profiles:login')
    context = {"form":form}
    return render(request,'profiles/register.html',context)
