from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course
from users.models import Payment, Subscribe, User
from users.serializers import PaymentSerializer, UserSerializer
from users.servises import create_price, create_stripe_session


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ("payment_date",)
    ordering = ("-payment_date",)
    filterset_fields = ("course", "lesson", "method", "amount")

    def perform_create(self, serializer):
        amount = serializer.validated_data["amount"]
        price = create_price(amount)
        session_id, payment_link = create_stripe_session(price)
        payment = serializer.save(user=self.request.user)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


class SubscribeView(APIView):
    def post(self, request, format=None):
        user = request.user
        if not user.is_authenticated:
            return Response(
                {"error": "Требуется авторизация"}, status=status.HTTP_401_UNAUTHORIZED
            )

        course_id = request.data.get("course_id")
        if not course_id:
            return Response(
                {"error": "Не указан course_id"}, status=status.HTTP_400_BAD_REQUEST
            )

        course = get_object_or_404(Course, id=course_id)
        subscription = Subscribe.objects.filter(user=user, course=course).first()

        if subscription:
            subscription.delete()
            message = "Подписка удалена"
            status_code = status.HTTP_200_OK
        else:
            Subscribe.objects.create(user=user, course=course)
            message = "Подписка добавлена"
            status_code = status.HTTP_201_CREATED

        return Response({"message": message}, status=status_code)
