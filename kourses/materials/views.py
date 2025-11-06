from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet


from materials.models import Lesson, Course
from materials.permissions import IsOwner, IsOwnerOrModer
from materials.serializers import (
    LessonSerializer,
    CourseSerializer,
)


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()


class LessonViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()

    def get_permissions(self):
        """Определяем права пользователя для каждого действия"""
        if self.action == "create":
            return [IsAuthenticated()]
        elif self.action in ["update", "retrieve"]:
            return [IsOwnerOrModer()]
        elif self.action == "destroy":
            return [IsOwner()]
        else:
            return [IsAuthenticated()]


