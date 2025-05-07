from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from requests import Response
from courses.models import Course
from users.models import CustomsUser, Payments
from users.serializers import CustomsUserSerializer, PaymentsSerializer
from users.services import creating_product_stripe, creating_price_stripe, creating_session_stripe


class UserCreateAPIView(CreateAPIView):
    serializer_class = CustomsUserSerializer
    queryset = CustomsUser.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentsViewSet(ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = (
        "paid_course",
        "paid_lesson",
        "payment_method",
    )
    ordering_fields = ("payment_date",)

class PaymentCreateAPIView(CreateAPIView):
    """Оплата курса через страйп"""

    queryset = CustomsUser.objects.all()
    serializer_class = PaymentsSerializer

    def post(self, request):
        course_id = request.data.get('course_id')
        amount = request.data.get('amount')
        course = Course.objects.get(id=course_id)

        product = creating_product_stripe(course)
        price = creating_price_stripe(amount, product.id)

        session_id, payment_link = creating_session_stripe(price)

        return Response({"session_id": session_id, "payment_link": payment_link}, status=status.HTTP_201_CREATED)

class CustomsUserViewSet(ModelViewSet):
    queryset = CustomsUser.objects.all()
    serializer_class = CustomsUserSerializer
