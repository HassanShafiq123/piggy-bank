from django.contrib.auth.models import User
from django.db.models import Sum, Avg, Count

from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime

from .models import Transaction, Category


@dataclass
class ReportEntry:
    category: Category
    total: Decimal
    count: int
    avg: Decimal


@dataclass
class ReportParams:
    start_date: datetime
    end_date: datetime
    user: User


def transaction_report(params: ReportParams):
    data = []

    queryset = Transaction.objects.filter(
        user=params.user,
        date__gte=params.start_date,
        date__lte=params.end_date
    ).values("category").annotate(
        total=Sum("ammount"),
        count=Count("id"),
        avg=Avg("ammount")
    )

    category_index = dict()

    for category in Category.objects.filter(user=params.user):
        category_index[category.pk] = category

    for entry in queryset:
        category = category_index.get(entry['category'])
        report_entry = ReportEntry(
            category, entry['total'], entry['count'], entry['avg']
            )
        data.append(report_entry)
    return data
