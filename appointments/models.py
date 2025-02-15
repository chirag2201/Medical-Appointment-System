from django.db import models
# Create your models here.

# user = User.objects.create(username="chirag_a",password="1234")
# user.first_name = "chirag"
# user.last_name = "a"
# user.is_active = True
# user.save()

class GenericUser(models.Model):
    username= models.CharField(max_length=50)
    phone_number =  models.CharField( max_length=50)
    email = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.username

class Doctor(models.Model):
    username = models.ForeignKey(GenericUser, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    available_from = models.TimeField()
    available_to = models.TimeField()
    
    def __str__(self) -> str:
        return self.specialization
    
class Patient(models.Model): 
    username =  models.ForeignKey(GenericUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)

    def __str__(self) -> str:
        return self.phone
    
class Appointment(models.Model):
    patient_user = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_user = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20,choices=[('Pending','Pending'),('Confirmed','Confirmed'),('Cancelled','Cancelled')],default='Pending')

    def __str__(self) -> str:
        return f"{self.patient_user.username} - {self.doctor_user.username}  {self.date}"
        
    
    

