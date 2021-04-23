from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Complaintbox(models.Model):
	p_name=models.CharField(max_length=100)
	p_email=models.EmailField(max_length=50)
	p_complaint=models.CharField(max_length=1000)

class ImProfile(models.Model):
	g = [('M',"Male"),('F','Female')]
	age = models.IntegerField(default=10)
	impf = models.ImageField(upload_to='Profiles/',default="profile.png")
	gender = models.CharField(max_length=10,choices=g)
	uid = models.OneToOneField(User,on_delete=models.CASCADE)

@receiver(post_save,sender=User)
def createpf(sender,instance,created,**kwargs):
	if created:
		ImProfile.objects.create(uid=instance)

class Bookreq(models.Model):
	Book_code=models.CharField(max_length=30)
	date=models.DateField()
	is_status=models.IntegerField(default=0)
	uploadby=models.CharField(max_length=120,default="")
	up=models.ForeignKey(User,on_delete=models.CASCADE,default="")

class Halldistrict(models.Model):
	name=models.CharField(max_length=90)

	def __str__(self):
		return self.name

class Hallname(models.Model):
	programming=models.ForeignKey(Halldistrict,on_delete=models.CASCADE)
	name=models.CharField(max_length=100)
	def __str__(self):
		return self.name

class Halldetails(models.Model):
	hallid=models.ForeignKey(Hallname,on_delete=models.CASCADE)
	h_name=models.CharField(max_length=50)
	h_capacity=models.IntegerField()
	h_location=models.CharField(max_length=2000)
	h_images=models.ImageField(upload_to='halls/',default="profile.png")
	h_number=models.CharField(max_length=12)
	def __str__(self):
		return self.h_name





