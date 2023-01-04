from .models import Profile,Relationship

def profile_pic(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        return {'profile_pic': profile.avatar}
    return {}
    
def invitations(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        invitations = Relationship.objects.invatations_received(profile).count()
        return {'invitations': invitations}
    return {}