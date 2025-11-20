from django.urls import include, path
from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import CourseViewSet, LessonViewSet

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r"courses", CourseViewSet)
router.register(r"lessons", LessonViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]

# urlpatterns += router.urls
