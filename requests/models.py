from django.db import models
from profiles.models import Profile

# Create your models here.


class FriendRequest(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="friend_requests_send")
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="friend_requests_receive")
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("sender", "receiver")

    def __str__(self):
        return f"{self.sender.username} send friend request to {self.receiver.username}"
