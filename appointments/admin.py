from django.contrib import admin
from appointments.models import Doctor, Patient, Appointment, GenericUser
# Register your models here.

@admin.register(GenericUser)
class GenericUserAdmin(admin.ModelAdmin):
    list_display = ['id','username','phone_number','email']

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['username','specialization','available_from','available_to']
    # search_fields = ['user__username','specialization']
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['username','phone']
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient_user','doctor_user','date','time', 'status']
    