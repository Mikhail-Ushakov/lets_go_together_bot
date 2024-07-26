from django.urls import path, include
from . import views
urlpatterns = [
    path('v1/register/', views.RegisterView.as_view()),
    path('v1/update/<int:user_id>/info/', views.ProfileView.as_view()),
    path('v1/user/<int:user_id>/', views.UserView.as_view()),
    path('v1/update/<int:user_id>/photo/', views.SetPhotoView.as_view()),
    path('v1/update/<int:user_id>/description/', views.SetDescriptionView.as_view()),
    path('v1/update/<int:user_id>/date/', views.SetDateView.as_view()),
    path('v1/update/<int:user_id>/interests/', views.SetInterestsView.as_view()),
    path('v1/update/<int:user_id>/skip-user/', views.DelayUserView.as_view()),
    path('v1/update/<int:user_id>/not-liked-user/', views.NotLikedView.as_view()),
    path('v1/update/<int:user_id>/liked-user/', views.LikedView.as_view()),
    path('v1/search-users/', views.SearchUser.as_view()),
]
