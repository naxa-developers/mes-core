from django.db import models


class Project(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=500)
	sector = models.CharField(max_length=200)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	reporting_period = models.IntegerField(choices=((1,"Monthly"),(2, "Bi-annually"), (3, "Quaterly")))
	beneficiaries = models.BooleanField(default=True)

	def __str__(self):
		return self.name

class Output(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=500)
  	PID = models.IntegerField('Project Id')

	def __str__(self):
		return self.name


class ActivityGroup(models.Model):
	output = models.ForeignKey('Output', related_name='activity_group')
	project = models.ForeignKey('Project', related_name='activity_group')
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=500)

	def __str__(self):
		return self.name


class Activity(models.Model):
	activity_group = models.ForeignKey('ActivityGroup', related_name='activity')
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=500)

	AG_Id = models.IntegerField('Activity Group ID')
	target_number = models.IntegerField()
	target_unit = models.CharField(max_length=200)

	start_date = models.DateTimeField()
	end_date = models.DateTimeField()

	form_id = models.IntegerField()

	target_complete = models.BooleanField(default=True)
	beneficiary_level = models.BooleanField(default=True)

	published = models.BooleanField(default=True)
	target_met = models.BooleanField(default=True)

	def __str__(self):
		return self.name


class Cluster(models.Model):
	name = models.CharField(max_length=200)
	project = models.ForeignKey('Project', related_name='cluster')	
	activity_group = models.ForeignKey('ActivityGroup', related_name='cluster')	
	district = models.CharField(max_length=200)
	municipality = models.CharField(max_length=200)
	ward = models.CharField(max_length=200)
