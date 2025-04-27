from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include

from users.apps import UsersConfig
from users.views import PaymentsViewSet, CustomsUserViewSet, UserCreateAPIView

app_name = UsersConfig.name

router = SimpleRouter()
router.register(r"user", CustomsUserViewSet, basename='user')
router.register(r"payments", PaymentsViewSet, basename='payments')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
]
urlpatterns += router.urls