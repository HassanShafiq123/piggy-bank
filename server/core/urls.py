from django.urls import path, include

from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from .import views

router = routers.SimpleRouter()
router.register('categories', views.CategoryModelViewSet, basename='category')
router.register(
    'transactions', views.TransactionModelViewSet, basename='transaction'
    )
router.register('currencies/', views.CurrencyModelViewSet, basename='currency')

urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('login/', obtain_auth_token, name='obtain-auth-token'),
    path('report/', views.TransactionReportAPIView.as_view(), name='report')
]+router.urls
