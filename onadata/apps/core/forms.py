from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Project, Output, ActivityGroup


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
		fields = ('name', 'description', 'PID')


class ActivityGroupForm(forms.ModelForm):

	class Meta:
		model = ActivityGroup
		fields = ('output', 'project', 'name', 'description')