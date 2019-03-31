from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from onadata.apps.logger.models import XForm
from .models import Project, Output, ActivityGroup, Activity, Cluster, Beneficiary, UserRole


class SignUpForm(UserCreationForm):
	email = forms.EmailField(max_length=300, help_text='Required. Inform a valid email address.')

	class Meta:
		model = User
		fields = ('username', 'email', 'password',)


class ProjectForm(forms.ModelForm):

	class Meta:
		model = Project
		fields = ('name', 'description', 'sector', 'start_date', 'end_date', 'reporting_period', 'beneficiaries')
		


class OutputForm(forms.ModelForm):

	class Meta:
		model = Output
		fields = ('name', 'description','project')


class ActivityGroupForm(forms.ModelForm):

	class Meta:
		model = ActivityGroup
		fields = ('output', 'project', 'name', 'description')



class ActivityForm(forms.ModelForm):
	def __init__(self, *args, **Kwargs):
		super(ActivityForm, self).__init__(*args, **Kwargs)
		self.fields['form'].queryset = XForm.objects.all()
		self.fields['form'].label_from_instance = lambda obj: "%s" % (obj.title)

	class Meta:
		model = Activity
		fields = ('activity_group', 'name', 'description', 'beneficiary_level', 'target_number', 'target_unit', 'start_date', 'end_date', 'form')


class ClusterForm(forms.ModelForm):

	class Meta:
		model = Cluster
		fields = ('name', 'project', 'district', 'municipality', 'ward')


class BeneficiaryForm(forms.ModelForm):

	class Meta:
		model = Beneficiary
		fields = ('name', 'address', 'ward_no', 'cluster', 'Type')


class UserRoleForm(forms.ModelForm):

	class Meta:
		model = UserRole
		fields = ('user', 'project', 'group', 'cluster')