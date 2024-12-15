from django.urls import path
from profiles import views
from posts import views as p_view


urlpatterns = [
    path('<int:pk>/', views.ProfileDetailView.as_view(), name="profile-detailed"),
    path("update/", views.ProfileUpdateView.as_view(), name="profile-update"),
    path("create_post/", p_view.ProfilePostCreateView.as_view(), name="create-post"),
    path("my_profile/", views.MyProfileDetailView.as_view(), name="my-profile"),
    path("<int:pk>/subscribe/", views.SubscriptionCreateView.as_view(), name="subscribe"),
    path("<int:pk>/unsubscribe/", views.SubscriptionDeleteView.as_view(), name="unsubscribe"),
    path("<int:pk>/send_friendrq/", views.FriendRequestCreateView.as_view(), name="friendrq"),
    path("<int:pk>/create_friendship/", views.FriendshipCreateView.as_view(), name="friendship"),
    path("<int:pk>/delete_friendrq/", views.FriendRequestDeleteView.as_view(), name="friendreq-delete"),
    path("users/", views.ProfilesListView.as_view(), name="profiles-list"),
    path("<int:pk>/delete_friendship/", views.FriendshipDeleteView.as_view(), name="friendship-delete"),

]

app_name = "profile"
