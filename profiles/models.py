from django.db import models
from django.contrib.auth.models import User
from .utils import *
from django.template.defaultfilters import slugify
from django.db.models import Q
# Create your models here.

class ProfileManager(models.Manager):
    def get_all_profiles_to_invite(self,sender):
        profiles = Profile.objects.all().exclude(user=sender)    
        profile = Profile.objects.get(user=sender)
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))
        accepted = set([])
        for rel in qs:
            if rel.status == "accepted":
                accepted.add(rel.receiver)
                accepted.add(rel.sender)
            
        available = [profile for profile in profiles if profile not in accepted]   
        return available
            
    def get_all_profiles(self,me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles



class Profile(models.Model):
    slug = models.SlugField(max_length=100, unique=True,blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100,blank=True)
    bio = models.TextField(default="no bio...")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to="profile_images",default="avatar.jpg")
    friends = models.ManyToManyField(User,blank=True,related_name='friends')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    objects = ProfileManager()
    
    def get_friends(self):
        return self.friends.all()
    
    def get_friends_no(self):
        return self.friends.all().count()
    
    def get_posts_no(self):
        return self.posts.all().count() 
    
    def get_likes_given_no(self):
        likes = self.like_set.all()
        total_likes = 0
        for like in likes:
            if like == "Like":
                total_likes += 1
        return total_likes
    
    def get_likes_received_no(self):
        posts = self.posts.all()
        total_likes = 0
        for post in posts:
            total_likes += post.liked.all().count()
        return total_likes
    
    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%Y')}"
    
    def save(self,*args,**kwargs):
        ex = False
        if self.first_name and self.last_name:
            to_slug = slugify(str(self.first_name) +' '+ str(self.last_name))
            ex = Profile.objects.filter(slug=to_slug).exists()
            while ex:
                to_slug = slugify(to_slug +' '+ str(get_unique_id()))
                ex = Profile.objects.filter(slug=to_slug).exists()
            self.slug = to_slug
        else:
            to_slug = slugify(self.user)
        self.slug = to_slug
        super().save(*args,**kwargs)
        
class RelationshipManger(models.Manager):
    def invatations_received(self,receiver):
        qs = Relationship.objects.filter(receiver=receiver,status="send")
        return qs    

class Relationship(models.Model):
    STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)
    sender = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='sender')
    receiver = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='receiver')
    status = models.CharField(max_length=10,choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    objects = RelationshipManger()
    
    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
    