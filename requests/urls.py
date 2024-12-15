from django.urls import path
from requests.views import FriendRequestListView

urlpatterns = [
    path("", FriendRequestListView.as_view(), name="friendrq-list")
]
