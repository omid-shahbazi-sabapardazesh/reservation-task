
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import SignUpView, LoginView

app_name = "core_auth"

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='custom_login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]