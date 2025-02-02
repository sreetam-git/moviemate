from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from user_app.api.views import registration_view, logout_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', obtain_auth_token, name='login'), # token authentication
    path('register/', registration_view, name='register'),  # registration endpoint
    path('logout/', logout_view, name='logout'),
    
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # jwt token authentication
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
