from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Employee(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name


class Tag(models.Model):
	name = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name

class GivenTask(models.Model):
	CATEGORY = (
			('Onspot', 'Onspot'),
			('Remotework', 'Remotework'),
			) 

	name = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True)
	category = models.CharField(max_length=200, null=True, choices=CATEGORY)
	description = models.CharField(max_length=200, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	tags = models.ManyToManyField(Tag)

	def __str__(self):
		return self.name

class Task(models.Model):
	STATUS = (
			('Pending', 'Pending'),
			('Reached Completion', 'Reached Completion'),
			('Completed', 'Completed'),
			)

	employee = models.ForeignKey(Employee, null=True, on_delete= models.SET_NULL)
	givenTask = models.ForeignKey(GivenTask, null=True, on_delete= models.SET_NULL)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)
	note = models.CharField(max_length=1000, null=True)

	def __str__(self):
		return self.givenTask.name



	
