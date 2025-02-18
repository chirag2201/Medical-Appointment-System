from rest_framework.response import Response
# from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from appointments.models import Doctor, Patient, Appointment, GenericUser
from django.contrib.auth.hashers import make_password


class UserListAPIView(APIView):
    queryset = GenericUser.objects.all()

    def get(self, request):
        users = self.queryset.values("id", "username", "phone_number","email")
        return Response(list(users), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        print("____________data___________")
        username = data.get("username")
        phone_number = data.get("phone")
        email = data.get("email")

        if not username or not phone_number or not email:
            return Response({'message': 'All the fields required, !'}, status=status.HTTP_400_BAD_REQUEST)
        
        print("________1_________________________________________________________")

        if GenericUser.objects.filter(username=username).exists():
            print("__________________________________________2_______________________")
            return Response({'message': 'Username has already been taken!'}, status=status.HTTP_400_BAD_REQUEST)
        print("_____________________________________________________________3____")
        user = GenericUser.objects.create(
            username=username,
            phone_number = phone_number,
            email = email,
        )

        # print("user: ",user)
        print("___4______________________________________________________________")
        return Response({'message': 'User created successfully!', "username": user.username,
            "phone number": user.phone_number,
            "email": user.email,}, status=status.HTTP_201_CREATED)


class DoctorListCreateAPIView(APIView):
    queryset = Doctor.objects.all()

    def get(self,request):
        doctors = self.queryset.values("id","username__username", "specialization")
        print("____GET____")
        return Response(list(doctors), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        print("data: ",data)
        username = data.get("doctor_username")
        specialization = data.get("doctor_specialization")
        available_from = data.get("available_from")
        available_to = data.get("available_to")
        print("username,specialization,available_from, available_to",username,specialization,available_from,available_to)
        if not username or not specialization:
            print("___2___")
            return Response({'message':'Username and specialization fields required!'},status=status.HTTP_400_BAD_REQUEST)
        
        user = GenericUser.objects.filter(username=username).first()
        if not user:
            print("_________3_________")
            return Response({'message':'User not found!'},status=status.HTTP_400_BAD_REQUEST)
        
        doctor = Doctor.objects.create(
            username=user,
            specialization=specialization,
            available_from=available_from,
            available_to= available_to
        )
        print("___4___")
        return Response({"message": "Doctor created", "username": doctor.username.username,"specialization":doctor.specialization, "available_from":doctor.available_from, "available_to":doctor.available_to}, status=status.HTTP_201_CREATED)


class PatientListCreateAPIView(APIView):
    queryset = Patient.objects.all()
    def get(self, request):
        data = request.data
        username = data.get("username")
        phone = data.get("phone")
        print("username,phone", username, phone)
        patients = self.queryset.values_list("id","username__username","phone")
        print(patients)
        return Response(list(patients), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        print("data: ", data)
        username = data.get("username")
        phone=data.get("phone")
        print("username and phone:",username, phone)
        if not username or not phone:
            print("_______2___________")
            return Response({'message':'username and phone fields are required!'}, status=status.HTTP_400_BAD_REQUEST)
        user = GenericUser.objects.filter(username=username).first()
        if not user:
            print("_________3_________")
            return Response({'message':'User not found!'},status=status.HTTP_400_BAD_REQUEST)

        patient = Patient.objects.create(
            username=user,
            phone=phone,
        )
        print("_________4____________")
        return Response({"message": "Patient created successfully!", "username": patient.username.username,"phone":patient.phone}, status=status.HTTP_201_CREATED)



class AppointmentListCreateAPIView(APIView):
    queryset = Appointment.objects.all()
    def get(self, request):
        data = request.data
        patient_username = data.get("patient_username")
        doctor_username = data.get("doctor_username")
        doctor_specialization = data.get("doctor_specialization")
        appointment_date = data.get("appointment_date")
        appointment_time = data.get("appointment_time")
        appointment_status = data.get("appointment_status")
        print(patient_username,doctor_username,doctor_specialization,appointment_date,appointment_time,appointment_status)
        
        appointments = self.queryset.values(
            "id", "patient_user__username", "doctor_user__username", "doctor_user__specialization", "date", "time", "status"
        )
        return Response(list(appointments), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        print("data: ",data)
        patient_username = data.get("patient_username")
        doctor_username = data.get("doctor_username")
        doctor_specialization = data.get("doctor_specialization")
        appointment_date = data.get("appointment_date") 
        appointment_time = data.get("appointment_time")
        appointment_status = data.get("appointment_status")
        print("All_fields: ",patient_username, doctor_username, doctor_specialization,appointment_date,appointment_time, appointment_status)
        if not patient_username or not doctor_username or not doctor_specialization:
            print("_______1________")
            return Response({'message':'patient_username, doctor_username and doctor_specialization is required!'}, status=status.HTTP_400_BAD_REQUEST)
        print("_____Patient_____")
        patient = Patient.objects.filter(username__username=patient_username).first()
        if not patient:
            print("_______2______")
            return Response({'message':'patient not found!'},status=status.HTTP_400_BAD_REQUEST)
        print("_____Doctor_____")
        doctor = Doctor.objects.filter(username__username=doctor_username, specialization=doctor_specialization).first()
        if not doctor:
            print("______3______")
            return Response({'message':'Doctor not found with this specialization!'},status=status.HTTP_400_BAD_REQUEST)

        print("_____Appointment_____")
        appointment = Appointment.objects.create(
            patient_user=patient,
            doctor_user=doctor,
            date=appointment_date,
            time=appointment_time,
            status=appointment_status
        )
        print("___4___")
        return Response({"message": "Appointment created successfully!","patient_username_id":appointment.patient_user.id, "patient_username":appointment.patient_user.username.username,"Doctor_username_id":appointment.doctor_user.id,  "doctor_username":appointment.doctor_user.username.username,"Doctor_specialization":appointment.doctor_user.specialization,"appointment_date":appointment.date, "appointment_time":appointment.time, "appointment_status":appointment.status}, status=status.HTTP_201_CREATED)
