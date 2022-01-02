from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Category, Currency, Transaction
from .reports import ReportParams


class CurencySerializer(serializers.ModelSerializer):
    """
    Class that serialize the Currency List API response
    """
    class Meta:
        model = Currency
        fields = ("id", "name", "code")


class CategorySerializer(serializers.ModelSerializer):
    """
    Class that serialize the Category API response
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = ('id', 'name', 'user')


class ReadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name")
        read_only_fields = fields


class WriteTransactionSerialzier(serializers.ModelSerializer):
    """
    Class that serialize Transaction API response

    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    currency = serializers.SlugRelatedField(
        slug_field="code", queryset=Currency.objects.all()
        )

    class Meta:
        model = Transaction
        fields = (
            'user',
            'ammount',
            'currency',
            'date',
            'description',
            'category'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        self.fields['category'].queryset = user.categories.all()


class ReadTransactionSerialzier(serializers.ModelSerializer):
    """
    Class that serialize Transaction API response
    """
    currency = CurencySerializer()
    category = CategorySerializer()
    user = ReadUserSerializer()

    class Meta:
        model = Transaction
        fields = (
            'id',
            'ammount',
            'currency',
            'date',
            'description',
            'category',
            'user',
        )

        read_only_fields = fields


class TransactionReportSerializer(serializers.Serializer):
    category = CategorySerializer()
    total = serializers.DecimalField(max_digits=15, decimal_places=2)
    count = serializers.IntegerField()
    avg = serializers.DecimalField(max_digits=15, decimal_places=2)


class ReportParamSerializer(serializers.Serializer):
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        return ReportParams(**validated_data)
