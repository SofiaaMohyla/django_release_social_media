from django.db import models
from profiles.models import Profile
from groups.models import Group, Channel
from django.contrib.auth.models import User


# Create your models here.

class Post(models.Model):
    TYPE_CHOICES = {
        "profile": "Profile",
        "group": "Group",
        "channel": "Channel"
    }

    title = models.CharField(max_length=50)
    description = models.TextField()
    media = models.FileField(upload_to="posts_media", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")
    type = models.CharField(choices=TYPE_CHOICES, max_length=8)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile_posts", null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group_posts", null=True, blank=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="channel_posts", null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.profile and not self.group and not self.channel:
            raise ValueError("Post must have a relation")
        return super().save(*args, **kwargs)


    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]


class Comment(models.Model):
    related_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments_on_post")
    content = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name="comments")

    def __str__(self):
        return f"Comment by {self.created_by.username} under {self.related_post.title} post"


class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f"{self.user.username} liked {self.post.title} post"


class Repost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reposts")
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="reposts")
    text = models.CharField(max_length=80, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} reposted {self.post.title}"
