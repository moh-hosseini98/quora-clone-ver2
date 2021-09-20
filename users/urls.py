from django.urls import path
from . import views


urlpatterns = [
    path('register/',views.RegisterAPIView.as_view()),
    path('me/',views.whoIAM.as_view())
]