from django.test import TestCase, Client
from django.urls import reverse
from appointments.models import GenericUser, Doctor, Patient, Appointment

class UserListAPIViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = GenericUser.objects.create(username="testuser", phone_number="1234567890", email="test@example.com")
        self.url = reverse("users")  

    def test_get_users(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("testuser", str(response.json()))

    def test_post_user(self):
        response = self.client.post(self.url, {"username": "newuser", "phone": "9876543210", "email": "new@example.com"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(GenericUser.objects.count(), 2)

class DoctorListCreateAPIViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = GenericUser.objects.create(username="doctoruser", phone_number="1234567890", email="doctor@example.com")
        self.url = reverse("doctors")

    def test_get_doctors(self):
        Doctor.objects.create(username=self.user, specialization="Cardiology", available_from="09:00:00", available_to="17:00:00")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Cardiology", str(response.json()))

    def test_post_doctor(self):
        response = self.client.post(self.url, {
            "doctor_username": "doctoruser",
            "doctor_specialization": "Neurology",
            "available_from": "08:00:00",
            "available_to": "16:00:00"
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Doctor.objects.count(), 1)

class PatientListCreateAPIViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = GenericUser.objects.create(username="patientuser", phone_number="1234567890", email="patient@example.com")
        self.url = reverse("patients")

    def test_get_patients(self):
        Patient.objects.create(username=self.user, phone="1234567890")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("patientuser", str(response.json()))

    def test_post_patient(self):
        response = self.client.post(self.url, {
            "username": "patientuser",
            "phone": "1231231234"
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Patient.objects.count(), 1)

class AppointmentListCreateAPIViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.patient_user = GenericUser.objects.create(username="chirag2201", phone_number="1234567890", email="patient@example.com")
        self.doctor_user = GenericUser.objects.create(username="chirag321", phone_number="9876543210", email="doctor@example.com")
        self.patient = Patient.objects.create(username=self.patient_user, phone="1234567890")
        self.doctor = Doctor.objects.create(username=self.doctor_user, specialization="Dermatology", available_from="08:00:00", available_to="16:00:00")
        self.url = reverse("appointments")

    def test_get_appointments(self):
        Appointment.objects.create(patient_user=self.patient, doctor_user=self.doctor, date="2025-02-15", time="10:00:00", status="Confirmed")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Dermatology", str(response.json()))

    def test_post_appointment(self):
        response = self.client.post(self.url, {
            "patient_username": "chirag2201",
            "doctor_username": "chirag321",
            "doctor_specialization": "Dermatology",
            "appointment_date": "2025-02-20",
            "appointment_time": "12:00:00",
            "appointment_status": "Pending"
        }) 
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Appointment.objects.count(), 1)
