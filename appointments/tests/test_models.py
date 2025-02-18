from appointments.models import GenericUser, Doctor, Patient, Appointment
from django.test import TestCase
from datetime import datetime

class GenericUserModelTest(TestCase):
    def test_generic_user(self):
        username = "chirag2201"
        phone_number = "1212"
        email = "chirag@gmail.com"
        
        user = GenericUser.objects.create(username=username, phone_number=phone_number,email=email)

        self.assertEqual(user.username, username)
        self.assertEqual(user.phone_number, phone_number)
        self.assertEqual(user.email, email)

class DocterUserModelTest(TestCase):
    def setUp(self):
        self.generic_user = GenericUser.objects.create(
            username = "chirag2201",
            phone_number ="836123",
            email ="chirag@example.com"
        )
    def test_doctor(self):
        username = self.generic_user
        specialization = "Neurologists"
        available_from = datetime.strptime("10:30:00","%H:%M:%S").time()
        available_to = datetime.strptime("11:30:00","%H:%M:%S").time()
        
        user = Doctor.objects.create(username=username, specialization=specialization,available_from=available_from,available_to=available_to)
        
        
        self.assertEqual(user.username,username)
        self.assertEqual(user.specialization,specialization)
        self.assertEqual(user.available_from,available_from)
        self.assertEqual(user.available_to,available_to)
        
class PatientUserModelTest(TestCase):
    def setUp(self):
        self.generic_user = GenericUser.objects.create(
            username = "chirag2201",
            phone_number = "23131",
            email = "chirag@makd.com"
        )
    
    def test_patient(self):
        patient = Patient.objects.create(
            username = self.generic_user,
            phone = self.generic_user.phone_number
        )
        
        self.assertEqual(patient.username, self.generic_user)
        self.assertEqual(patient.phone, self.generic_user.phone_number)
        
class AppointmentsUserModelTest(TestCase):
    def setUp(self):
        self.generic_user1 = GenericUser.objects.create(
            username = "chirag2201",
            phone_number= "123123",
            email = "chirag@example.com",
        )
        self.generic_user2 = GenericUser.objects.create(
            username = "chirag22",
            phone_number = "123",
            email = "chirag@example.com",
        )
        self.patient_user = Patient.objects.create(username=self.generic_user1,phone=self.generic_user1.phone_number)
        self.doctor_user = Doctor.objects.create(username=self.generic_user2,specialization="Cardiologist",available_from="20:30:00",available_to="10:30:00")
        
    def test_appointments(self):
        appointment_date = datetime.strptime("2020-12-21","%Y-%m-%d").date()
        appointment_time = datetime.strptime("10:30:00","%H:%M:%S").time()
        appointment_status = "Confirmed"
        
        appointment = Appointment.objects.create(patient_user=self.patient_user.username,doctor_user=self.doctor_user.username,date=appointment_date,time=appointment_time,status=appointment_status)
            
        self.assertEqual(appointment.patient_user, self.patient_user.username)
        self.assertEqual(appointment.doctor_user, self.doctor_user.username)
        self.assertEqual(appointment.date, appointment_date)
        self.assertEqual(appointment.time, appointment_time)
        self.assertEqual(appointment.status, appointment_status)