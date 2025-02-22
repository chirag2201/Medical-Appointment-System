from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from appointments.models import Doctor, Patient, Appointment, GenericUser


class UserListAPIView(APIView):

    def get(self, request):
        users = GenericUser.objects.values("id", "user_name", "phone_number","email")
        return Response(list(users), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        user_name = data.get("username")
        phone_number = data.get("phone_number")
        email = data.get("email")

        if not user_name or not phone_number or not email:
            return Response({'message': 'Username, phone number and Email is required !'}, status=status.HTTP_400_BAD_REQUEST)
        

        if GenericUser.objects.filter(user_name=user_name).exists():
            return Response({'message': 'Username has already been taken!'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = GenericUser.objects.create(
            user_name= user_name,
            phone_number = phone_number,
            email = email,
        )
        return Response({'message': 'User created successfully!', "username": user.user_name,
            "phone number": user.phone_number,
            "email": user.email,}, status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        data = request.data
        user_name = data.get("username")
        user_email = data.get("email")
        
        if not user_name or not user_email:
            return Response({'message':'Username and Email ID is required to delete a user!'}, status=status.HTTP_400_BAD_REQUEST)

        if user_name:
            user = GenericUser.objects.filter(user_name=user_name).first()
        else:
            user = GenericUser.objects.filter(email=user_email).first()
        
        if not user:
            return Response({'message':'User not found!'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.delete()
        return Response({'message':'User deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
            

class DoctorListCreateAPIView(APIView):
    
    
    def get(self,request):
        doctors = Doctor.objects.values("id","doctor_username__user_name", "specialization")
        return Response(list(doctors), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        doctor_username = data.get("doctor_username")
        specialization = data.get("doctor_specialization")
        available_from = data.get("available_from")
        available_to = data.get("available_to")
        if not doctor_username or not specialization:
            return Response({'message':'Username and specialization fields required!'},status=status.HTTP_400_BAD_REQUEST)
        
        user = GenericUser.objects.filter(user_name=doctor_username).first()
        if not user:
            return Response({'message':'User not found!'},status=status.HTTP_400_BAD_REQUEST)
        
        doctor = Doctor.objects.create(
            doctor_username=user,
            specialization=specialization,
            available_from=available_from,
            available_to= available_to
        )
        return Response({"message": "Doctor created", "username": doctor.doctor_username.user_name,"specialization":doctor.specialization, "available_from":doctor.available_from, "available_to":doctor.available_to}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        data = request.data
        doctor_username = data.get("doctor_username")
        doctor_specialization = data.get("doctor_specialization")
        
        if not doctor_username or not doctor_specialization:
            return Response({'message':'doctor_username and doctor_specialization is required to delete doctor!'}, status=status.HTTP_400_BAD_REQUEST)

        if doctor_username:
            doctor = Doctor.objects.filter(doctor_username__user_name=doctor_username).first()
        else:
            doctor = Doctor.objects.filter(specialization=doctor_specialization).first()
        
        if not doctor:
            return Response({'message':'Doctor not found with this specialization!'}, status=status.HTTP_400_BAD_REQUEST)
        
        doctor.delete()
        return Response({'message':'doctor deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
class PatientListCreateAPIView(APIView):
    
    
    def get(self, request):
        patients = Patient.objects.values("id","patient_username__user_name","phone_number")
        return Response(list(patients), status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        patient_username = data.get("patient_username")
        phone_number=data.get("phone_number")

        if not patient_username or not phone_number:
            return Response({'message':'username and phone fields are required!'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = GenericUser.objects.filter(user_name=patient_username).first()
        if not user:
            return Response({'message':'User not found!'},status=status.HTTP_400_BAD_REQUEST)

        patient = Patient.objects.create(
            patient_username=user,
            phone_number=phone_number,
        )
        return Response({"message": "Patient created successfully!", "username": patient.patient_username.user_name,"phone":patient.phone_number}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        data = request.data
        patient_username = data.get("patient_username")
        phone_number = data.get("phone_number")
        
        if not patient_username or not phone_number:
            return Response({'message':'patient_username and phone_number is required to delete a user!'}, status=status.HTTP_400_BAD_REQUEST)

        if patient_username:
            patient = Patient.objects.filter(patient_username__user_name=patient_username).first()
        else:
            patient = Patient.objects.filter(phone_number=phone_number).first()
        
        if not patient:
            return Response({'message':'patient not found!'}, status=status.HTTP_400_BAD_REQUEST)
        
        patient.delete()
        return Response({'message':'patient deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

class AppointmentListCreateAPIView(APIView):
    
    
    def get(self, request):
        appointments = Appointment.objects.values(
            "id", "patient_user__patient_username__user_name", "doctor_user__doctor_username__user_name", "doctor_user__specialization", "date", "time", "status"
        )
        return Response(list(appointments), status=status.HTTP_200_OK)
        

    def post(self, request):
        data = request.data
        patient_username = data.get("patient_username")
        doctor_username = data.get("doctor_username")
        doctor_specialization = data.get("doctor_specialization")
        appointment_date = data.get("appointment_date") 
        appointment_time = data.get("appointment_time")
        appointment_status = data.get("appointment_status")
        
        if not patient_username or not doctor_username or not doctor_specialization:
            return Response({'message':'patient_username, doctor_username and doctor_specialization is required!'}, status=status.HTTP_400_BAD_REQUEST)

        patient = Patient.objects.filter(patient_username__user_name=patient_username).first()
        if not patient:
            return Response({'message':'patient not found!'},status=status.HTTP_400_BAD_REQUEST)
        
        doctor = Doctor.objects.filter(doctor_username__user_name=doctor_username, specialization=doctor_specialization).first()
        if not doctor:
            return Response({'message':'Doctor not found with this specialization!'},status=status.HTTP_400_BAD_REQUEST)


        appointment = Appointment.objects.create(
            patient_user=patient,
            doctor_user=doctor,
            date=appointment_date,
            time=appointment_time,
            status=appointment_status
        )

        return Response({"message": "Appointment created successfully!","patient_username_id":appointment.patient_user.id, "patient_username":appointment.patient_user.patient_username.user_name,"Doctor_username_id":appointment.doctor_user.id,  "doctor_username":appointment.doctor_user.doctor_username.user_name,"Doctor_specialization":appointment.doctor_user.specialization,"appointment_date":appointment.date, "appointment_time":appointment.time, "appointment_status":appointment.status}, status=status.HTTP_201_CREATED)

            
    def delete(self, request):
        data = request.data
        patient_username = data.get("patient_username")
        doctor_username = data.get("doctor_username")
        doctor_specialization = data.get("doctor_specialization")
        
        if not patient_username or not doctor_username or not doctor_specialization:
            return Response({'message':'Patient_username, Doctor_username and Doctor Specialization is required to delete an Appointment!'}, status=status.HTTP_400_BAD_REQUEST)

        if doctor_username:
            doctor = Doctor.objects.filter(doctor_username__user_name=doctor_username).first()
        else: 
            doctor = Doctor.objects.filter(specialization=doctor_specialization).first()
        
        if not doctor:
            return Response({'message':'Appointment not found!'}, status=status.HTTP_400_BAD_REQUEST)
            
        
        doctor.delete()
        return Response({'message':'Appointment deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        