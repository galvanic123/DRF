from rest_framework import serializers

from users.models import Payments, CustomsUser

class CustomsUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomsUser
        fields = '__all__'

class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'
