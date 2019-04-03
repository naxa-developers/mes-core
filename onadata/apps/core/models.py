from django.contrib.auth.models import User, Group
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token
from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime

from datetime import datetime  

from onadata.apps.logger.models import Instance
from onadata.apps.logger.models.xform import XForm

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
	project = models.ForeignKey('Project', related_name='output')

	def __str__(self):
		return self.name


class Cluster(models.Model):
	name = models.CharField(max_length=200)
	project = models.ForeignKey('Project', related_name='cluster')	
	district = models.CharField(max_length=200)
	municipality = models.CharField(max_length=200)
	ward = models.CharField(max_length=200)

	def toDict(self):
		return {'id':self.id,
				'name': self.name,
				'project': self.project,
				'district':self.district,
				'municipality':self.municipality,
				'ward':self.ward}

	def __str__(self):
		return self.name


class ActivityGroup(models.Model):
	output = models.ForeignKey('Output', related_name='activity_group')
	project = models.ForeignKey('Project', related_name='activity_group')
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=500)
	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
	weight = models.FloatField(default=0)


	def __str__(self):
		return self.name


class Activity(models.Model):
	activity_group = models.ForeignKey('ActivityGroup', related_name='activity')
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=500)

	target_number = models.IntegerField(null=True, blank=True)
	target_unit = models.CharField(max_length=200, null=True, blank=True)

	start_date = models.DateTimeField()
	end_date = models.DateTimeField()

	form = models.ForeignKey(XForm, related_name='actform', null=True, blank=True)

	beneficiary_level = models.BooleanField(default=True)
	weight = models.FloatField(default=0)

	def __str__(self):
		return self.name



class Beneficiary(models.Model):
	name = models.CharField(max_length=200)
	address = models.CharField(max_length=400)
	ward_no = models.IntegerField('ward number')
	cluster = models.ForeignKey('Cluster', related_name='beneficiary')
	Type = models.CharField(max_length=100)
	GovernmentTranch = models.CharField(max_length=100, blank=True)
	ConstructionPhase = models.CharField(max_length=100, blank=True)
	Typesofhouse = models.CharField(max_length=100, blank=True)
	Remarks = models.CharField(max_length=100, blank=True)


	def __str__(self):
		return self.name



class UserRole(models.Model):
	user = models.ForeignKey(User, related_name="user_roles")
	project = models.ForeignKey('Project', null=True, blank=True)
	group = models.ForeignKey(Group, related_name="userrole_group")
	cluster = models.ForeignKey(Cluster, null=True, blank=True, related_name="userrole_cluster")

	def save(self, *args, **kwargs):
		if UserRole.objects.filter(group=self.group, cluster=self.cluster).exists():
			raise ValidationError('A cluster can contain only a single ' + self.group.name)
		if self.group.name == 'community-social-mobilizer':
			if UserRole.objects.filter(user=self.user, group=self.group).exists():
				raise ValidationError('CSM user can be assigned to only one cluster.')
		return super(UserRole, self).save(*args, **kwargs)

	def __str__(self):
		return self.group.name


class ClusterAG(models.Model):
	activity_group = models.ForeignKey('ActivityGroup', related_name='clusterag')
	cluster = models.ForeignKey('cluster', related_name='clusterag')


class ClusterA(models.Model):
	activity = models.ForeignKey('Activity', related_name='clustera')
	cag = models.ForeignKey('ClusterAG', related_name='ca')
	start_date = models.DateTimeField(default=datetime.now)
	end_date = models.DateTimeField(default=datetime.now)


class Submission(models.Model):
	cluster_activity = models.ForeignKey('ClusterA', related_name='submissions')
	instance = models.OneToOneField(Instance, related_name="submission")
	beneficiary = models.ForeignKey('Beneficiary',null=True, blank=True, on_delete=models.SET_NULL, related_name="submissions" )
	status = models.CharField(max_length=10, default='pending')


class Config(models.Model):
	available_version = models.FloatField('Available Version')
	updates = models.CharField(max_length=500)
	activity_group_updated = models.DateTimeField(default=datetime.now(), blank=True)
