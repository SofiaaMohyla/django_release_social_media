from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView
from requests.models import FriendRequest
from profiles.forms import FriendshipCreationForm
# Create your views here.


class FriendRequestListView(LoginRequiredMixin, ListView):
    model = FriendRequest
    context_object_name = "friend_requests"
    template_name = "requests/friendrq_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["friendship_form"] = FriendshipCreationForm()

        return context

    def get_queryset(self):
        queryset = super(FriendRequestListView, self).get_queryset()
        queryset = queryset.filter(accepted=False)

        return queryset
