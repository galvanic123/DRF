from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from users.models import Payments, CustomsUser
from users.serializers import PaymentsSerializer, CustomsUserSerializer

class CustomsUserViewSet(ModelViewSet):
    queryset = CustomsUser.objects.all()
    serializer_class = CustomsUserSerializer

class PaymentsViewSet(ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    filterset_fields = (
        'paid_course',
        'paid_lesson',
        'payment_method',
    )
    ordering_fields = ('payment_date',)