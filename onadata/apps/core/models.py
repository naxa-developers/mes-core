from django.contrib.auth.models import User, Group, Permission
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token
from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime

from datetime import datetime

from django.contrib.gis.db.models import PointField
from onadata.apps.logger.models import Instance
from onadata.apps.logger.models.xform import XForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import get_interval
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


class Project(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=500)
	sector = models.CharField(max_length=200)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	reporting_period = models.IntegerField(choices=((1,"Monthly"),(2, "Bi-annually"), (3, "Quarterly")))
	beneficiaries = models.BooleanField(default=True)

	def __str__(self):
		return self.name


class ProjectTimeInterval(models.Model):
	project = models.ForeignKey(Project, related_name='interval')
	label = models.CharField(max_length=20)
	start_date = models.DateField()
	end_date = models.DateField()

	def __str__(self):
		return self.label


class Output(models.Model):
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=500)
	project = models.ForeignKey('Project', related_name='output')

	def __str__(self):
		return self.name


class District(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name


class Municipality(models.Model):
	name = models.CharField(max_length=100)
	district = models.ForeignKey(District, related_name="municipality")

	def __str__(self):
		return self.name


class Cluster(models.Model):
	name = models.CharField(max_length=200)
	project = models.ForeignKey('Project', related_name='cluster')
	municipality = models.ManyToManyField(Municipality, related_name="cluster")
	ward = models.CharField(max_length=200)

	def toDict(self):
		return {'id':self.id,
				'name': self.name,
				'project': self.project_id,
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

	form = models.ForeignKey(XForm, related_name='actform', null=True, blank=True)

	beneficiary_level = models.BooleanField(default=True)
	weight = models.FloatField(default=0)

	time_interval = models.ForeignKey(ProjectTimeInterval, related_name='activity_interval', null=True, blank=True)
	location = PointField(geography=True, srid=4326, blank=True, null=True)

	def __str__(self):
		return self.name

	@property
	def latitude(self):
		if self.location:
			return self.location.y

	@property
	def longitude(self):
		if self.location:
			return self.location.x


PAYMENT_CHOICES = (
	('single', 'One Time Payment'),
	('daily', 'Daily Basis')
)


class Beneficiary(models.Model):
	name = models.CharField(max_length=200)
	address = models.CharField(max_length=400, null=True, blank=True)
	district = models.ForeignKey(District, blank=True, null=True)
	municipality = models.ForeignKey(Municipality, blank=True, null=True)
	ward_no = models.IntegerField('ward number', null=True, blank=True)
	cluster = models.ForeignKey('Cluster', related_name='beneficiary')
	Type = models.CharField(max_length=100, null=True, blank=True)
	vulnerabilityType = models.CharField(max_length=100)
	GovernmentTranch = models.CharField(max_length=100, blank=True)
	ConstructionPhase = models.CharField(max_length=100, blank=True)
	Typesofhouse = models.CharField(max_length=100, blank=True)
	Remarks = models.CharField(max_length=100, blank=True)
	location = PointField(geography=True, srid=4326, blank=True, null=True)
	payment_type = models.CharField(max_length=100, choices=PAYMENT_CHOICES, blank=True, null=True)

	def __str__(self):
		return self.name

	@property
	def latitude(self):
		if self.location:
			return self.location.y

	@property
	def longitude(self):
		if self.location:
			return self.location.x


class UserRole(models.Model):
	user = models.ForeignKey(User, related_name="user_roles")
	project = models.ForeignKey('Project', null=True, blank=True)
	group = models.ForeignKey(Group, related_name="userrole_group")
	cluster = models.ManyToManyField("Cluster", null=True, blank=True, related_name="userrole_cluster")

	def __str__(self):
		return self.group.name


class ClusterAG(models.Model):
	activity_group = models.ForeignKey('ActivityGroup', related_name='clusterag')
	cluster = models.ForeignKey('cluster', related_name='clusterag')


class ClusterA(models.Model):
	activity = models.ForeignKey('Activity', related_name='clustera')
	cag = models.ForeignKey('ClusterAG', related_name='ca')
	target_number = models.IntegerField(null=True, blank=True, default=0)
	target_unit = models.CharField(max_length=200, null=True, blank=True, default='')
	time_interval = models.ForeignKey(ProjectTimeInterval, related_name='cainterval', null=True, blank=True)
	target_completed = models.IntegerField(null=True, blank=True, default=0)
	interval_updated = models.BooleanField(default=False)
	target_updated = models.BooleanField(default=False)
	location = PointField(geography=True, srid=4326, blank=True, null=True)

	@property
	def latitude(self):
		if self.location:
			return self.location.y

	@property
	def longitude(self):
		if self.location:
			return self.location.x

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		if not self.id:
			if not self.activity.beneficiary_level:
				self.target_unit = self.activity.target_unit
			self.time_interval = self.activity.time_interval
		return super(ClusterA, self).save()


class ClusterAHistory(models.Model):
	clustera = models.ForeignKey(ClusterA, related_name='history')
	time_interval = models.ForeignKey(ProjectTimeInterval, related_name="cahistory", null=True, blank=True)
	target_completed = models.IntegerField(null=True, blank=True, default=0)
	target_number = models.IntegerField(null=True, blank=True, default=0)
	updated_date = models.DateTimeField(auto_now_add=True)


class Submission(models.Model):
	cluster_activity = models.ForeignKey('ClusterA', related_name='submissions')
	clustera_history = models.ForeignKey('ClusterAHistory', related_name='submissions', null=True, blank=True)
	instance = models.OneToOneField(Instance, related_name="submission")
	beneficiary = models.ForeignKey('Beneficiary',null=True, blank=True, on_delete=models.SET_NULL, related_name="submissions" )
	status = models.CharField(max_length=10, default='pending')


class Config(models.Model):
	available_version = models.FloatField('Available Version')
	updates = models.CharField(max_length=500)
	activity_group_updated = models.DateTimeField(default=datetime.now(), blank=True)


@receiver(post_save, sender=Project)
def save_interval(sender, instance, **kwargs):
	ProjectTimeInterval.objects.filter(project=instance).delete()
	if instance.reporting_period == 1:
		intervals = get_interval(instance.start_date, instance.end_date, 12)
		i = 1
		for item in range(len(intervals)):
			try:
				label = "Month" + str(i)
				i = i + 1
				start_date = intervals[0]
				end_date = intervals[1]
				ProjectTimeInterval.objects.get_or_create(
					project=instance,
					label=label,
					start_date=start_date,
					end_date=end_date)
				intervals.pop(0)
			except:
				pass
	elif instance.reporting_period == 2:
		intervals = get_interval(instance.start_date, instance.end_date, 2)
		i = 1
		for item in range(len(intervals)):
			try:
				label = "Half" + str(i)
				i = i + 1
				start_date = intervals[0]
				end_date = intervals[1]
				ProjectTimeInterval.objects.get_or_create(
					project=instance,
					label=label,
					start_date=start_date,
					end_date=end_date)
				intervals.pop(0)
			except:
				pass
	else:
		intervals = get_interval(instance.start_date, instance.end_date, 4)
		i = 1
		for item in range(len(intervals)):
			try:
				label = "Quarter" + str(i)
				i = i + 1
				start_date = intervals[0]
				end_date = intervals[1]
				ProjectTimeInterval.objects.get_or_create(
					project=instance,
					label=label,
					start_date=start_date,
					end_date=end_date)
				intervals.pop(0)
			except:
				pass


@receiver(post_save, sender=UserRole)
def asset_permissions(sender, instance, **kwargs):
	if instance.group.name in ['project-manager', 'project-management-unit', 'project-coordinator']:
		codenames = ['add_asset', 'change_asset', 'delete_asset', 'view_asset', 'share_asset']
		permissions = Permission.objects.filter(codename__in=codenames)
		for permission in permissions:
			instance.user.user_permissions.add(permission)
