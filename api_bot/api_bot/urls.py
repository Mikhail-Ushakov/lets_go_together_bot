from django.urls import path, include
from . import views
urlpatterns = [
    path('v1/register/', views.RegisterView.as_view()),
    path('v1/update/<int:user_id>/', views.ProfileView.as_view()),
]
