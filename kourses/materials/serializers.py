from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Lesson, Course


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "id",
            "name",
            "description",
            "preview",
            "link",
        ]


class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lesson_count = SerializerMethodField()

    def get_lesson_count(self, instance):
        if hasattr(instance, "lesson_count"):
            return instance.lesson_count
        return instance.lesson_set.count()

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "description",
            "lessons",
            "lesson_count",
        ]
