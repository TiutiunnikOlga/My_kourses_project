from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import PaymentViewSet, SubscribeView, UserViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"payments", PaymentViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("subscription/", SubscribeView.as_view(), name="subscribe"),
]
