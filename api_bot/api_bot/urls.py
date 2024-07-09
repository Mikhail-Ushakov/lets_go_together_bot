from django.urls import path, include
from . import views
urlpatterns = [
    path('v1/register/', views.RegisterView.as_view()),
    path('v1/update/<int:user_id>/', views.ProfileView.as_view()),
    path('v1/user/<int:user_id>/', views.UserView.as_view()),
    path('v1/setphoto/<int:user_id>/', views.SetPhotoView.as_view()),
]
