from django.urls import path, include
from . import views
urlpatterns = [
    path('v1/register/', views.RegisterView.as_view())
]
