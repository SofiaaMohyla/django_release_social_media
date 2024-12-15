from django.urls import path
from posts import views


urlpatterns = [
    path("", views.PostsListView.as_view(), name="posts-list"),
    path("<int:pk>/", views.PostDetailView.as_view(), name="post-detailed"),
    path("<int:pk>/delete/", views.PostDeleteView.as_view(), name="delete-post"),
    path("<int:pk>/update/", views.PostUpdateView.as_view(), name="update-post"),
    path("<int:pk>/like/", views.LikeCreateView.as_view(), name="liking-post"),
    path("<int:pk>/comment/", views.CommentCreateView.as_view(), name="commenting-post"),
    path("<int:pk>/comment/delete/", views.CommentDeleteView.as_view(), name="comment-delete"),
    path("<int:pk>/comment/update/", views.CommentUpdateView.as_view(), name="comment-update"),
    path("<int:pk>/like/delete/", views.LikeDeleteView.as_view(), name="like-delete"),
    path("<int:pk>/repost/", views.RepostCreateView.as_view(), name="repost-create"),
    path("<int:pk>/repost/delete", views.RepostDeleteView.as_view(), name="repost-delete"),

]


app_name = "posts"
