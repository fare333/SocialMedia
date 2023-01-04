from django.db import models

from profiles.models import Profile
# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="posts")
    content = models.TextField()
    image = models.ImageField(upload_to="posts",blank=True)
    liked = models.ManyToManyField(Profile,blank=True, related_name='likes')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.content[:20])
    
    def num_likes(self):
        return self.liked.all().count()
    
    def num_comments(self):
        return self.comment_set.all().count()    
    
    def get_all_authors_posts(self):
        return self.comment_set.all()

    
    class Meta:
        ordering =("-created",)
        
class Comment(models.Model):
    author = models.ForeignKey(Profile,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    body = models.TextField(max_length=100)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.pk)

LIKE_CHOICES =(
    ('Like','Like'),('Unlike','Unlike')
)
class Like(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    value = models.CharField(max_length=8,choices=LIKE_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"
