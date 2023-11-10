
from django.urls import path
from accounts.apiviews.registration import RegistrationView
from accounts.apiviews.authorization import AuthorizationView
from accounts.apiviews.profile import ProfileView

urlpatterns = [
    path('register', RegistrationView.as_view(), name='register'),
    path('token/<str:slug>', AuthorizationView.as_view(), name='authirize'),
    path('me', ProfileView.as_view(), name='user_profile')
]
