from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.forms import widgets
from django.db.models import Sum

from onadata.apps.logger.models import XForm
from .models import Project, Output, ActivityGroup, Activity, Cluster, Beneficiary, UserRole, Config


class SignUpForm(UserCreationForm):
	email = forms.EmailField(max_length=300, help_text='Required. Inform a valid email address.')

	class Meta:
		model = User
		fields = ('username', 'email', 'password',)


# class DivWrapperWidget(widgets.TextInput):
# 	def render(self, id, max_length, name, placeholder, type):
# 		return mark_safe(u'''<div class="form-group"><select class="custom-select">%s</select></div>''' % (super(DivWrapperWidget, self).render(id, max_length, name, placeholder, type)))

# class BootstrapDivWidget(forms.Form):
# 	def as_div(self):
#         "Return this form rendered as HTML <tr>s -- excluding the <table></table>."
#         return self._html_output(
#             normal_row='<div>%(html_class_attr)s><br>%(label)s</br><br>%(errors)s%(field)s%(help_text)s</br></div>',
#             error_row='<div colspan="2">%s</div>',
#             row_ender='<div></div>',
#             help_text_html='<br><span class="helptext">%s</span>',
#             errors_on_separate_row=False,
# )

class ProjectForm(forms.ModelForm):

	class Meta:
		model = Project
		
		fields = ('name', 'description', 'sector', 'start_date', 'end_date', 'reporting_period', 'beneficiaries')
		
		widgets = {
			'name': forms.TextInput(attrs={'placeholder': 'Name','class': 'form-control'}),
			'description': forms.Textarea(attrs={'placeholder': 'Description','class': 'form-control'}),
			'sector': forms.TextInput(attrs={'placeholder': 'Sector','class': 'form-control'}),
			'start_date': forms.TextInput(attrs={'placeholder': 'Start date','class': 'form-control', 'type': 'date'}),
			'end_date': forms.TextInput(attrs={'placeholder': 'End date','class': 'form-control', 'type': 'date'}),
			'reporting_period': forms.Select(attrs={'class': "custom-select"}),
		}


class OutputForm(forms.ModelForm):

	class Meta:
		model = Output
		fields = ('name', 'description','project')

		widgets = {
			'name': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}),
			'description': forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control'}),
			'project': forms.Select(attrs={'class': "custom-select"}),
		}

		# def __init__(self, *args, **kwargs):
		# 	super().__init__(*args, **kwargs)
		# 	self.fields['project'].queryset = Project.objects.none()


class ActivityGroupForm(forms.ModelForm):

	class Meta:
		model = ActivityGroup
		fields = ('name', 'description', 'output', 'project', 'weight')

		widgets = {
			'name' : forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}),
			'description' : forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control'}),
			'output' : forms.Select(attrs={'class': "custom-select"}),
			'project' : forms.Select(attrs={'class': "custom-select"}),
			'weight': forms.TextInput(attrs={'placeholder': 'Weight', 'class': 'form-control'})
		}

		# def __init__(self, *args, **kwargs):
		# 	super().__init__(*args, **kwargs)
		# 	self.fields['output'].queryset = Output.objects.none()
		# 	self.fields['project'].queryset = Project.objects.none()

	def clean_weight(self):
		if not isinstance(self.cleaned_data.get('weight'), int) and not isinstance(self.cleaned_data.get('weight'), float):
			raise ValidationError({'weight': ['Please enter a valid weight']})
		else:
			return self.cleaned_data.get('weight')

	def clean(self):
		try:
			other_activity_groups = ActivityGroup.objects.filter(output=self.cleaned_data.get('output')).aggregate(
				weights=Sum('weight'))
			print(other_activity_groups)
			if self.cleaned_data['weight'] + other_activity_groups['weights'] > 100:
				raise ValidationError({
					'weight': ['The combined weight of activity groups in this output should not exceed 100.']})
		except KeyError:
			raise ValidationError('error occured')



class ActivityForm(forms.ModelForm):
	def __init__(self, *args, **Kwargs):
		super(ActivityForm, self).__init__(*args, **Kwargs)
		self.fields['form'].queryset = XForm.objects.all()
		self.fields['form'].label_from_instance = lambda obj: "%s" % (obj.title)

	class Meta:
		model = Activity
		fields = ('activity_group', 'name', 'description', 'beneficiary_level', 'target_number', 'target_unit', 'start_date', 'end_date', 'form', 'weight')

		widgets = {
			'activity_group' : forms.Select(attrs={'class': "custom-select"}),
			'name': forms.TextInput(attrs={'placeholder': 'Name','class': 'form-control'}),
			'description': forms.Textarea(attrs={'placeholder': 'Description','class': 'form-control'}),
			'target_number': forms.TextInput(attrs={'placeholder': 'Target Number','class': 'form-control'}),
			'target_unit': forms.TextInput(attrs={'placeholder': 'Target Unit','class': 'form-control'}),
			'start_date': forms.TextInput(attrs={'placeholder': 'Start date','class': 'form-control', 'type': 'date'}),
			'end_date': forms.TextInput(attrs={'placeholder': 'End date','class': 'form-control', 'type': 'date'}),
			'form': forms.Select(attrs={'class': "custom-select"}),
			'weight': forms.TextInput(attrs={'placeholder': 'Weight', 'class': 'form-control'})
		}

	def clean_weight(self):
		if not isinstance(self.cleaned_data.get('weight'), int) and not isinstance(self.cleaned_data.get('weight'), float):
			raise ValidationError({'weight': ['Please enter a valid weight']})
		else:
			return self.cleaned_data.get('weight')

	def clean(self):
		cleaned_data = self.cleaned_data
		try:
			act_g = self.cleaned_data.get('activity_group')
			# ag = ActivityGroup.objects.get(activity_group=self.cleaned_data.get('activity_group'))
			other_activities = Activity.objects.filter(activity_group=act_g).aggregate(
				weights=Sum('weight'))
			if other_activities.get('weight') is not None:
				if self.cleaned_data.get('weight') + other_activities['weights'] > act_g.weight:
					raise ValidationError({
						'weight': ['The combined weight of activities in this activity group should not exceed %s.', act_g.weight]})
			else:
				if self.cleaned_data.get('weight') > act_g.weight:
					raise ValidationError({
						'weight': ['The combined weight of activities in this activity group should not exceed the activity group weight.']})
			return cleaned_data
		except KeyError:
			raise ValidationError('error occured')


class ClusterForm(forms.ModelForm):

	class Meta:
		model = Cluster
		fields = ('name', 'district', 'municipality', 'ward', 'project')


		widgets = {
			'name': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}),
			'district': forms.TextInput(attrs={'placeholder': 'District', 'class': 'form-control'}),
			'municipality': forms.TextInput(attrs={'placeholder': 'Municipality', 'class': 'form-control'}),
			'ward': forms.TextInput(attrs={'placeholder': 'Ward', 'class': 'form-control'}),
			'project': forms.Select(attrs={'class': "custom-select"}),
		}

		# def __init__(self, *args, **kwargs):
		# 	super().__init__(*args, **kwargs)
		# 	self.fields['project'].queryset = Project.objects.none()


class BeneficiaryForm(forms.ModelForm):

	class Meta:
		model = Beneficiary
		fields = ('name', 'address', 'ward_no', 'Type', 'GovernmentTranch', 'ConstructionPhase', 'Typesofhouse', 'Remarks', 'cluster')


		widgets = {
			'name': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}),
			'address': forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control'}),
			'ward_no': forms.TextInput(attrs={'placeholder': 'Ward Number', 'class': 'form-control'}),
			'Type': forms.TextInput(attrs={'placeholder': 'Type', 'class': 'form-control'}),
			'GovernmentTranch': forms.TextInput(attrs={'placeholder': 'Government Tranch', 'class': 'form-control'}),
			'ConstructionPhase': forms.TextInput(attrs={'placeholder': 'Construction Phase', 'class': 'form-control'}),
			'Typesofhouse': forms.TextInput(attrs={'placeholder': 'Types of house', 'class': 'form-control'}),
			'Remarks': forms.TextInput(attrs={'placeholder': 'Remarks', 'class': 'form-control'}),
			'cluster': forms.Select(attrs={'class': "custom-select"}),
		}


class UserRoleForm(forms.ModelForm):

	class Meta:
		model = UserRole
		fields = ('user', 'project', 'group', 'cluster')

		widgets = {
			'user': forms.Select(attrs={'class': "custom-select"}),		
			'project': forms.Select(attrs={'class': "custom-select"}),
			'group': forms.Select(attrs={'class': "custom-select"}),
			'cluster': forms.Select(attrs={'class': "custom-select"}),
		}


class ConfigForm(forms.ModelForm):

	class Meta:
		model = Config
		fields = ('available_version', 'updates')
