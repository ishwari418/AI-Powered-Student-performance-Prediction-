from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict_view, name='predict'),
    path('results/', views.PredictionListView.as_view(), name='prediction_results'),
    path('result/<int:pk>/', views.PredictionDetailView.as_view(), name='prediction_detail'),
]
