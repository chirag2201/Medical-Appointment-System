from appointments.models import GenericUser, Doctor, Patient, Appointment
from django.test import TestCase

class GenericUserModelTest(TestCase):
    def test_generic_user(self):
        username = "chirag2201"
        phone_number = "1212"
        email = "chirag@gmail.com"
        
        user = GenericUser.objects.create(username=username, phone_number=phone_number,email=email)

        self.assertEqual(user.username, username)
        self.assertEqual(user.phone_number, phone_number)
        self.assertEqual(user.email, email)

# class DocterUserModelTest(TestCase):
#     def test_doctor(self):
#     username = "chirag2201"
#     specialization = "Neurologists"
#     available_from = ""
#     available_to = models.TimeField()