from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from groups.models import Group, Member, Channel, Viewer
from groups.forms import GroupCreationForm, MemberCreationForm, ChannelCreationForm, ViewerCreationForm
from posts.models import Post


# Create your views here.

class GroupsListView(ListView):
    model = Group
    context_object_name = "groups"
    template_name = "groups/groups_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["join_form"] = MemberCreationForm()

        return context


class GroupDetailView(DetailView):
    model = Group
    context_object_name = "group"
    template_name = "groups/group_detailed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["members"] = Member.objects.filter(group=self.object)
        context["posts"] = Post.objects.filter(type="group", group=self.object)

        return context


class GroupCreateView(LoginRequiredMixin, CreateView):
    model = Group
    form_class = GroupCreationForm
    template_name = "groups/group_creation_page.html"
    success_url = reverse_lazy("groups:groups-list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user.profile
        group = form.save()

        Member.objects.create(user=self.request.user.profile, group=group).save()
        group.save()

        return super().form_valid(form)


class GroupUpdateView(LoginRequiredMixin, UpdateView):
    model = Group
    template_name = "groups/group_creation_page.html"

    def get_success_url(self):
        return reverse_lazy("groups:groups-detail", kwargs={"pk": self.object.pk})


class GroupDeleteView(LoginRequiredMixin, DeleteView):
    model = Group
    template_name = "groups/group_delete_confirmation.html"
    success_url = reverse_lazy("groups:groups-list")


class MemberCreateView(LoginRequiredMixin, CreateView):
    model = Member
    form_class = MemberCreationForm

    def get_group(self):
        group_pk = self.kwargs.get("pk")

        return get_object_or_404(Group, pk=group_pk)

    def form_valid(self, form):
        form.instance.user = self.request.user.profile
        form.instance.group = self.get_group()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("groups:group-detailed", kwargs={"pk": self.kwargs.get("pk")})


class MemberDeleteView(LoginRequiredMixin, DeleteView):
    model = Member
    template_name = "groups/group_leaving_confirmation.html"
    success_url = reverse_lazy("groups:groups-list")
    context_object_name = "member"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["group_pk"] = self.kwargs.get("pk")

        return context

    def get_object(self, queryset=None):
        obj = Member.objects.get(user=self.request.user.profile, group=self.kwargs.get("pk"))

        return obj


class ChannelListView(ListView):
    model = Channel
    context_object_name = "channels"
    template_name = "groups/channels_list.html"


class ChannelDetailView(DetailView):
    model = Channel
    context_object_name = "channel"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["viewers"] = Viewer.objects.filter(channel=self.object)
        context["joining"] = ViewerCreationForm()
        context['current_viewer'] = self.request.user.profile.views.filter(channel=self.object).first()
        context['posts'] = Post.objects.filter(type="channel", channel=self.object)

        return context


class ChannelCreateView(LoginRequiredMixin, CreateView):
    model = Channel
    form_class = ChannelCreationForm
    template_name = "groups/channel_creation_page.html"
    success_url = reverse_lazy("groups:channels-list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user.profile
        channel = form.save()

        Viewer.objects.create(user=self.request.user.profile, channel=channel, is_admin=True).save()
        channel.save()

        return super().form_valid(form)


class ChannelUpdateView(LoginRequiredMixin, UpdateView):
    model = Channel
    form_class = ChannelCreationForm
    context_object_name = "channel"
    template_name = "groups/channel_creation_page.html"

    def get_success_url(self):
        return reverse_lazy("groups:channel-detailed", pk=self.kwargs.get("pk"))


class ChannelDeleteView(LoginRequiredMixin, DeleteView):
    model = Channel
    template_name = "groups/channel_delete_confirmation.html"
    success_url = reverse_lazy("groups:channels-list")


class ViewerCreateView(LoginRequiredMixin, CreateView):
    model = Viewer
    form_class = ViewerCreationForm

    def get_channel(self):
        channel_pk = self.kwargs.get("pk")

        return get_object_or_404(Channel, pk=channel_pk)

    def form_valid(self, form):
        form.instance.user = self.request.user.profile
        form.instance.channel = self.get_channel()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("groups:channel-detailed", kwargs={"pk": self.kwargs.get("pk")})


class ViewerDeleteView(LoginRequiredMixin, DeleteView):
    model = Viewer
    template_name = "groups/group_leaving_confirmation.html"
    success_url = reverse_lazy("groups:channels-list")
    context_object_name = "viewer"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["channel_pk"] = self.kwargs.get("pk")

        return context

    def get_object(self, queryset=None):
        obj = Viewer.objects.get(user=self.request.user.profile, channel=self.kwargs.get("pk"))

        return obj


class MembersListView(ListView):
    model = Member
    context_object_name = "members"
    template_name = "groups/members_list_view.html"

    def get_queryset(self):
        queryset = super(MembersListView, self).get_queryset()
        queryset = queryset.filter(group=Group.objects.get(pk=self.kwargs.get("pk")))

        return queryset


class ViewersListView(ListView):
    model = Viewer
    context_object_name = "viewers"
    template_name = "groups/viewers_list_view.html"

    def get_queryset(self):
        queryset = super(ViewersListView, self).get_queryset()
        queryset = queryset.filter(channel=Channel.objects.get(pk=self.kwargs.get("pk")))

        return queryset
