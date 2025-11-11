from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course
from users.models import User, Payment, Subscribe


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

class SubscribeSerializer(ModelSerializer):
    class Meta:
        model = Subscribe
        fields = "__all__"

class CourseSerializer(ModelSerializer):
    is_subscribed = SerializerMethodField()

    def get_subscribed(self, obj):
        request = self.context.get('request')
        if not request.user.is_authenticated:
            return False
        return Subscribe.objects.filter(user=request.user, course=obj).exists()
    class Meta:
        model = Course
        fields = ['id', 'title', 'is_subscribed', 'description']
