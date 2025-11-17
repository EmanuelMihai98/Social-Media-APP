from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    display_name = models.CharField(max_length=30, blank=True)
    bio = models.TextField(max_length=200, blank=True)
    created_at = models.DateField(auto_now_add=True)
    profile_pic = models.ImageField(upload_to="profile_pic/", blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def get_display_name(self):
        return self.display_name if self.display_name else self.user.username
    

    def get_followers(self):
        from follows.models import Follow

        followers = Follow.objects.filter(following=self.user)
        followers_ids = followers.values_list("follower", flat=True)

        return User.objects.filter(id__in=followers_ids)
    
    def count_followers(self):

        return self.user.followers_set.count()

    def get_following(self):
        from follows.models import Follow

        following = Follow.objects.filter(follower=self.user)
        following_ids = following.values_list("following", flat=True)

        return User.objects.filter(id__in=following_ids)
    
    def count_following(self):
        return self.user.following_set.count()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()