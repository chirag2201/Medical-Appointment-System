from django.contrib import admin
from appointments.models import Doctor, Patient, Appointment, GenericUser
# Register your models here.

@admin.register(GenericUser)
class GenericUserAdmin(admin.ModelAdmin):
    list_display = ['id','user_name','phone_number','email']

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['doctor_username','specialization','available_from','available_to']
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['patient_username','phone_number']
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient_user','doctor_user','date','time', 'status']
    