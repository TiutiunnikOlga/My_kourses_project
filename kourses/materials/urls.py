from rest_framework.routers import DefaultRouter
from django.urls import path, include

from materials.views import (
    CourseViewSet,
    LessonViewSet,
)
from materials.apps import MaterialsConfig

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r"courses", CourseViewSet)
router.register(r"lessons", LessonViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]

# urlpatterns += router.urls
