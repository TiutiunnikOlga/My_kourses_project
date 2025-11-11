from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet


from materials.models import Lesson, Course
from materials.paginations import CustomPagination
from materials.permissions import IsOwner, IsOwnerOrModer
from materials.serializers import (
    LessonSerializer,
    CourseSerializer,
)


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_serializer_context(self):
        return{'request': self.request}


class LessonViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        """Определяем права пользователя для каждого действия"""
        if self.action == "create":
            return [IsAuthenticated()]
        elif self.action in ["update", "retrieve"]:
            return [IsOwnerOrModer()]
        elif self.action == "destroy":
            return [IsOwner()]
        else:
            return [AllowAny()]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()
