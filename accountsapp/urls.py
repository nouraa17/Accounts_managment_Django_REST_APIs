from django.urls import path, include
from . import views
from .views import LoginAPI, RegisterAPI
from rest_framework.routers import DefaultRouter
# router = DefaultRouter()
# router.register('patient', views.viewsets_patient)

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/patient/', views.patient_create),
    # path('api/patient/<int:pk>', views.patient_pk),
    path('api/predict/', views.ImageUploadView.as_view()),

    # path('api/',  include(router.urls)),

]
