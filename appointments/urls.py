from django.urls import path
from appointments.views import UserListAPIView, DoctorListCreateAPIView, PatientListCreateAPIView, AppointmentListCreateAPIView

urlpatterns = [
    path('users/',UserListAPIView.as_view(),name='users'),
    path('doctors/',DoctorListCreateAPIView.as_view(),name='doctors'),
    path('patients/',PatientListCreateAPIView.as_view(),name='patients'),
    path('appointments/',AppointmentListCreateAPIView.as_view(),name='appointments'),
]
