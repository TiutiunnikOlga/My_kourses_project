from rest_framework.routers import DefaultRouter
from django.urls import path, include

from users.views import (
    UserViewSet,
    UserListApiView,
    UserCreateApiView,
    UserUpdateApiView,
    UserDestroyApiView,
    UserRetrieveApiView,
    PaymentViewSet,
)
from users.apps import UsersConfig

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"payments", PaymentViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("user/", UserListApiView.as_view(), name="user_list"),
    path("user/<int:pk>", UserRetrieveApiView.as_view(), name="user_retrieve"),
    path("user/create/", UserCreateApiView.as_view(), name="user_create"),
    path("user/<int:pk>/delete", UserDestroyApiView.as_view(), name="user_delete"),
    path("user/<int:pk>/update/", UserUpdateApiView.as_view(), name="user_update"),
    # path("payment/", PaymentListApiView.as_view(), name="payment_list"),
]

# urlpatterns += router.urls
