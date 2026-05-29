from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = "community"

urlpatterns = [
    path("", views.asset_list, name="asset_list"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", views.profile, name="profile"),
    path("profile/analysis/", views.profile_analysis, name="profile_analysis"),
    path("password/change/", views.UserPasswordChangeView.as_view(), name="password_change"),
    path("password/change/done/", views.UserPasswordChangeDoneView.as_view(), name="password_change_done"),
    path("asset/<str:asset_id>/", views.board, name="board"),
    path("asset/<str:asset_id>/post/new/", views.post_create, name="post_create"),
    path("asset/<str:asset_id>/post/<int:post_id>/", views.post_detail, name="post_detail"),
    path("asset/<str:asset_id>/post/<int:post_id>/edit/", views.post_update, name="post_update"),
    path("asset/<str:asset_id>/post/<int:post_id>/delete/", views.post_delete, name="post_delete"),
]
