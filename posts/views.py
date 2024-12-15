from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db import models
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from groups.models import Group, Channel
from posts.forms import PostCreationForm, PostUpdateForm, LikeCreationForm, CommentCreationForm, RepostCreationForm
from posts.models import Post, Comment, Like, Repost
from posts.mixins import UserIsOwnerMixin, ObjectExistMixin, UserIsNotLikeOwnerMixin, UsersActionMixin, \
    UserIsNotOwnerMixin
from profiles.models import Profile


# Create your views here.


class PostsListView(ListView):
    model = Post
    paginate_by = 10
    context_object_name = "posts"
    template_name = "posts/posts_list.html"

    def get_queryset(self):
        queryset = super(PostsListView, self).get_queryset()
        try:
            profile = self.request.user.profile
        except AttributeError:
            return queryset
        groups = Group.objects.filter(members__user=profile)
        channels = Channel.objects.filter(viewers__user=profile)
        friends = Profile.objects.filter(models.Q(friends_from__user1=profile) | models.Q(friends_to__user2=profile))
        subscriptions = Profile.objects.filter(subscriptions__subscriber=profile)

        posts = Post.objects.filter(
            models.Q(group__in=groups) | models.Q(channel__in=channels) | models.Q(profile__in=friends) | models.Q(profile__in=subscriptions)).distinct()

        return posts


class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "posts/post_detailed.html"

    def get_watched_post(self):
        post_pk = self.kwargs.get("pk")

        return get_object_or_404(Post, pk=post_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["liking_form"] = LikeCreationForm()
        context["comment_form"] = CommentCreationForm()
        context["repost_form"] = RepostCreationForm()
        context["comments"] = get_object_or_404(Post, pk=self.kwargs.get("pk")).comments_on_post.all()
        if self.request.user.is_authenticated:
            context["repost"] = self.request.user.profile.reposts.filter(post=self.get_watched_post())
            context["like"] = self.request.user.profile.likes.filter(post=self.get_watched_post())
        context["likes_count"] = self.object.likes.count()
        context["repost_count"] = self.object.reposts.count()

        return context


class ProfilePostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    success_url = reverse_lazy("profile:my-profile")
    form_class = PostCreationForm
    template_name = "posts/post_creation_form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user.profile
        form.instance.profile = self.request.user.profile
        form.instance.type = "profile"

        return super().form_valid(form)


class GroupPostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreationForm
    template_name = "posts/post_creation_form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user.profile
        form.instance.group = get_object_or_404(Group, pk=self.kwargs.get("pk"))
        form.instance.type = "group"

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("groups:group-detailed", kwargs={"pk": self.kwargs.get("pk")})


class ChannelPostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreationForm
    template_name = "posts/post_creation_form.html"

    def get_success_url(self):
        return reverse_lazy("groups:channel-detailed", kwargs={"pk": self.kwargs.get("pk")})

    def form_valid(self, form):
        form.instance.created_by = self.request.user.profile
        form.instance.channel = get_object_or_404(Channel, pk=self.kwargs.get("pk"))
        form.instance.type = "channel"

        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Post
    template_name = "posts/post_delete_confirmation.html"
    success_url = reverse_lazy("posts:posts-list")


class PostUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Post
    form_class = PostUpdateForm
    context_object_name = "post"
    template_name = "posts/post_update_form.html"

    def get_success_url(self):
        return reverse_lazy("posts:post-detailed", kwargs={"pk": self.object.pk})


class LikeCreateView(LoginRequiredMixin, UserIsNotLikeOwnerMixin, ObjectExistMixin, CreateView):
    model = Like
    form_class = LikeCreationForm

    def get_post(self):
        post_pk = self.kwargs.get("pk")

        return get_object_or_404(Post, pk=post_pk)

    def get_success_url(self):
        return reverse_lazy("posts:post-detailed", kwargs={"pk": self.object.post.pk})

    def form_valid(self, form):
        form.instance.post = self.get_post()
        form.instance.user = self.request.user.profile

        return super().form_valid(form)


class LikeDeleteView(LoginRequiredMixin, UsersActionMixin, DeleteView):
    model = Like

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_pk"] = self.object.post.pk

        return context

    def get_post(self):
        post_pk = self.kwargs.get("pk")

        return get_object_or_404(Post, pk=post_pk)

    def get_success_url(self):
        return reverse_lazy("posts:post-detailed", kwargs={"pk": self.object.post.pk})


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentCreationForm

    def get_post(self):
        post_pk = self.kwargs.get("pk")

        return get_object_or_404(Post, pk=post_pk)

    def get_success_url(self):
        return reverse_lazy("posts:post-detailed", kwargs={"pk": self.object.related_post.pk})

    def form_valid(self, form):
        form.instance.created_by = self.request.user.profile
        form.instance.related_post = self.get_post()

        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Comment
    template_name = "posts/comment_update_form.html"
    form_class = CommentCreationForm

    def get_success_url(self):
        return reverse_lazy("posts:post-detailed", kwargs={"pk": self.object.related_post.pk})


class CommentDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Comment
    template_name = "posts/comment_delete_confirmation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_pk"] = self.object.related_post.pk

        return context

    def get_success_url(self):
        return reverse_lazy("posts:post-detailed", kwargs={"pk": self.object.related_post.pk})


class RepostCreateView(LoginRequiredMixin, CreateView):
    model = Repost
    form_class = RepostCreationForm

    def get_post(self):
        post_pk = self.kwargs.get("pk")

        return get_object_or_404(Post, pk=post_pk)

    def get_success_url(self):
        return reverse_lazy("posts:post-detailed", kwargs={"pk": self.object.post.pk})

    def form_valid(self, form):
        if self.request.user.profile == self.get_post().created_by:
            raise PermissionDenied("You can't repost your own post.")
        form.instance.user = self.request.user.profile
        form.instance.post = self.get_post()

        return super().form_valid(form)


class RepostDeleteView(LoginRequiredMixin, UsersActionMixin, DeleteView):
    model = Repost

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_pk"] = self.object.post.pk

        return context

    def get_post(self):
        post_pk = self.kwargs.get("pk")

        return get_object_or_404(Post, pk=post_pk)

    def get_success_url(self):
        return reverse_lazy("posts:post-detailed", kwargs={"pk": self.object.post.pk})
