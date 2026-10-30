from django.db import models

# Create your models here.
class DoctorDB(models.Model):
    doctor_name = models.CharField(max_length=50)
    specialization = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()
    hospital = models.CharField(max_length=100)
    consultation_fee = models.PositiveIntegerField()
    available = models.BooleanField(default= True)

    def __str__(self):
        return self.doctor_name

class AppointmentDb(models.Model):
    patient_name = models.CharField(max_length=50)
    phone = models.CharField(max_length= 15)
    doctor_id = models.IntegerField()
    appointment_date = models.DateField()
    token_number = models.PositiveIntegerField(editable=False, null=True)
    appointment_time = models.TimeField(editable= True, null= True)
    problem = models.TextField(null= True, blank= True)
    status = models.CharField(max_length=100, default="pending")
    presciption = models.TextField(null= True, blank= True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patient_name