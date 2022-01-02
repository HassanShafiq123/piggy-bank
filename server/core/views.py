from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Currency, Transaction
from .serializers import (
    CurencySerializer,
    CategorySerializer,
    ReadTransactionSerialzier,
    TransactionReportSerializer,
    WriteTransactionSerialzier,
    ReportParamSerializer
    )
from .reports import transaction_report
from .permissions import IsAdminOrReadOnly


class CurrencyModelViewSet(ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Currency.objects.all()
    serializer_class = CurencySerializer
    pagination_class = None


class CategoryModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    pagination_class = None

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class TransactionModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ("description",)
    ordering_fields = ("ammount", "date")
    filterset_fields = ("currency__code",)

    def get_queryset(self):
        return Transaction.objects.select_related(
            "currency",
            "category",
            "user",
            ).filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ('list', 'get'):
            return ReadTransactionSerialzier
        return WriteTransactionSerialzier


class TransactionReportAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        param_serializser = ReportParamSerializer(
            data=request.GET, context={"request": request}
            )
        param_serializser.is_valid(raise_exception=True)
        param = param_serializser.save()
        data = transaction_report(param)
        serializer = TransactionReportSerializer(instance=data, many=True)
        return Response(data=serializer.data)
