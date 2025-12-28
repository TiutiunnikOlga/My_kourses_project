from drf_yasg.openapi import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.paginations import CustomPagination
from materials.permissions import IsOwner, IsOwnerOrModer
from materials.serializers import CourseSerializer, LessonSerializer
from materials.tasks import send_mail_on_update


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_serializer_context(self):
        return {"request": self.request}

    @action(detail=True, methods=["post"], url_path="update-and-notify")
    def update_course(self, request, pk=None):
        course = get_object_or_404(Course, id=pk)
        old_update = course.updated_at
        course.save()
        if course.updated_at != old_update:
            send_mail_on_update.delay(course.id)
            return Response(
                {"message": "Курс обновлен, письмо отправлено"},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"message": "Курс не обновлен, письмо не отправлено"},
            status=status.HTTP_200_OK,
        )


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
            return [IsAuthenticated()]
