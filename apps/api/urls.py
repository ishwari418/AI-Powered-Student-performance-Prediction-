from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'students', views.StudentViewSet)
router.register(r'predictions', views.PredictionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
