from django.db import models
from django_countries.fields import CountryField

class Patients(models.Model) :
    GENDER_CHOICES=[('M','Male'),('F','Female')]
    # id=models.BigAutoField(primary_key=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100,blank=True)
    dob=models.DateField()
    gender = models.CharField(choices=GENDER_CHOICES,max_length=2)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100,blank=True)
    city = models.CharField(max_length=100)
    country =models.CharField(max_length=250)
    email=models.EmailField(max_length=255)
    reason=models.TextField(max_length=500)
    image=models.ImageField(upload_to='images/')
    # date=models.DateTimeField()
    def __str__(self):
        return self.firstname

class Report(models.Model):
    # id=models.BigAutoField(primary_key=True)
    report_id = models.CharField(max_length=100)
    diagnosis = models.CharField(max_length=100)
    lesionType = models.CharField(max_length=100, blank=True)
    # created_at= models.DateField()
