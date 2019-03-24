from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.forms import widgets

from onadata.apps.logger.models import XForm
from .models import Project, Output, ActivityGroup, Activity, Cluster, Beneficiary, UserRole


class SignUpForm(UserCreationForm):
	email = forms.EmailField(max_length=300, help_text='Required. Inform a valid email address.')

	class Meta:
		model = User
		fields = ('username', 'email', 'password',)


# class DivWrapperWidget(widgets.TextInput):
# 	# def render(self, id, max_length, name, placeholder, type):
# 		return mark_safe(u'''<div class="form-group">%s</div>''' % (super(DivWrapperWidget, self).render(id, max_length, name, placeholder, type)))

class ProjectForm(forms.ModelForm):
	# FORM_CHOICES = (
	# 		('yes', 'yes'),('no', 'no'),
	# 	)


	# beneficiaries = forms.ChoiceField(widget=forms.RadioSelect(),choices=FORM_CHOICES)

	class Meta:
		model = Project
		
		fields = ('name', 'description', 'sector', 'start_date', 'end_date', 'reporting_period', 'beneficiaries')
		
		widgets = {
			'name': forms.TextInput(attrs={'placeholder': 'Name','class': 'form-control'}),
			'description': forms.Textarea(attrs={'placeholder': 'Description','class': 'form-control'}),
			'sector': forms.TextInput(attrs={'placeholder': 'Sector','class': 'form-control'}),
			'start_date': forms.TextInput(attrs={'placeholder': 'Start date','class': 'form-control', 'type': 'date'}),
			'end_date': forms.TextInput(attrs={'placeholder': 'End date','class': 'form-control', 'type': 'date'}),
		}


class OutputForm(forms.ModelForm):

	class Meta:
		model = Output
		fields = ('name', 'description','project')

		widgets = {
			'name': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}),
			'description': forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control'}),
		}

		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.fields['project'].queryset = Project.objects.none()



class ActivityGroupForm(forms.ModelForm):

	class Meta:
		model = ActivityGroup
		fields = ('name', 'description', 'output', 'project')

		widgets = {
			'name' : forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}),
			'description' : forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control'}),
		}

		# def __init__(self, *args, **kwargs):
		# 	super().__init__(*args, **kwargs)
		# 	self.fields['output'].queryset = Output.objects.none()
		# 	self.fields['project'].queryset = Project.objects.none()			


class ActivityForm(forms.ModelForm):
	def __init__(self, *args, **Kwargs):
		super(ActivityForm, self).__init__(*args, **Kwargs)
		self.fields['form'].queryset = XForm.objects.all()
		self.fields['form'].label_from_instance = lambda obj: "%s" % (obj.title)

	class Meta:
		model = Activity
		fields = ('activity_group', 'name', 'description', 'target_number', 'target_unit', 'start_date', 'end_date', 'form', 'beneficiary_level')

		widgets = {
			'name': forms.TextInput(attrs={'placeholder': 'Name','class': 'form-control'}),
			'description': forms.Textarea(attrs={'placeholder': 'Description','class': 'form-control'}),
			'target_number': forms.TextInput(attrs={'placeholder': 'Target Number','class': 'form-control'}),
			'target_unit': forms.TextInput(attrs={'placeholder': 'Target Unit','class': 'form-control'}),
			'start_date': forms.TextInput(attrs={'placeholder': 'Start date','class': 'form-control', 'type': 'date'}),
			'end_date': forms.TextInput(attrs={'placeholder': 'End date','class': 'form-control', 'type': 'date'}),
		}


class ClusterForm(forms.ModelForm):

	class Meta:
		model = Cluster
		fields = ('name', 'district', 'municipality', 'ward', 'project')


		widgets = {
			'name': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}),
			'district': forms.TextInput(attrs={'placeholder': 'District', 'class': 'form-control'}),
			'municipality': forms.TextInput(attrs={'placeholder': 'Municipality', 'class': 'form-control'}),
			'ward': forms.TextInput(attrs={'placeholder': 'Ward', 'class': 'form-control'}),
		}

		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.fields['project'].queryset = Project.objects.none()


class BeneficiaryForm(forms.ModelForm):

	class Meta:
		model = Beneficiary
		fields = ('name', 'address', 'ward_no', 'Type', 'cluster')


		widgets = {
			'name': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}),
			'address': forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control'}),
			'ward_no': forms.TextInput(attrs={'placeholder': 'Ward Number', 'class': 'form-control'}),
			'Type': forms.TextInput(attrs={'placeholder': 'Type', 'class': 'form-control'}),
		}


class UserRoleForm(forms.ModelForm):

	class Meta:
		model = UserRole
		fields = ('user', 'project', 'group')