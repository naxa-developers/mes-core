from django import forms
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.forms import widgets
from django.db.models import Sum
from django.core.validators import validate_email
import re

from onadata.apps.logger.models import XForm
from .models import Project, Output, ActivityGroup, Activity, Cluster, Beneficiary, UserRole, Config, \
    ProjectTimeInterval, Municipality


class LoginForm(forms.Form):
    username = forms.CharField(label='Your Email/Username', max_length=100)
    password = forms.CharField(label='Your Password', max_length=100)


class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='Email address', required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, label='Your Password', max_length=100)
    password2 = forms.CharField(widget=forms.PasswordInput, label='One more time?', max_length=100)

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = self.cleaned_data.get('password1')
        password1 = self.cleaned_data.get('password2')
        if password != password1:
            raise ValidationError({'password1': ['The passwords did not match']})

        else:
            if password:
                if len(password) < 8:
                    raise ValidationError({'password1': ['Passwords must be of more than 8 characters']})

                pattern = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$")
                if not bool(pattern.search(password)):
                    raise ValidationError(
                        {'password1': ['Password must contain alphabet characters, special characters and numbers']})

    def clean_email(self):
        email = self.cleaned_data['email']
        if validate_email(email) == False:
            raise ValidationError('Enter a valid Email address')

        if User.objects.filter(email=email):
            raise ValidationError('User with this email already exists')
        else:
            return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise ValidationError('User with this username already exists')
        else:
            return username


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
            'name': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control'}),
            'sector': forms.TextInput(attrs={'placeholder': 'Sector', 'class': 'form-control'}),
            'start_date': forms.TextInput(attrs={'placeholder': 'Start date', 'class': 'form-control', 'type': 'date'}),
            'end_date': forms.TextInput(attrs={'placeholder': 'End date', 'class': 'form-control', 'type': 'date'}),
            'reporting_period': forms.Select(attrs={'class': "custom-select"}),
        }


class OutputForm(forms.ModelForm):
    class Meta:
        model = Output
        fields = ('name', 'description', 'project')

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
            'name': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control'}),
            'output': forms.Select(attrs={'class': "custom-select"}),
            'project': forms.Select(attrs={'class': "custom-select"}),
            'weight': forms.TextInput(attrs={'placeholder': 'Weight', 'class': 'form-control'})
        }

    # def __init__(self, *args, **kwargs):
    # 	super().__init__(*args, **kwargs)
    # 	self.fields['output'].queryset = Output.objects.none()
    # 	self.fields['project'].queryset = Project.objects.none()

    def clean_weight(self):
        if not isinstance(self.cleaned_data.get('weight'), int) and not isinstance(self.cleaned_data.get('weight'),
                                                                                   float):
            raise ValidationError({'weight': ['Please enter a valid weight']})
        else:
            return self.cleaned_data.get('weight')

    def clean(self):
        try:
            output = self.cleaned_data.get('output')
            project = self.cleaned_data.get('project')
            name = self.cleaned_data.get('name')
            description = self.cleaned_data.get('description')
            try:
                ag = ActivityGroup.objects.get(output=output, project=project, name=name, description=description)
                other_activity_groups = ActivityGroup.objects.filter(output=self.cleaned_data.get('output')).aggregate(
                    weights=Sum('weight'))

                if other_activity_groups['weights']:
                    weight = other_activity_groups['weights'] - ag.weight

                    if self.cleaned_data.get('weight') + weight > 100:
                        raise ValidationError({
                            'weight': ['The combined weight of activity groups in this output should not exceed 100.']})

            except ActivityGroup.DoesNotExist:
                other_activity_groups = ActivityGroup.objects.filter(output=self.cleaned_data.get('output')).aggregate(
                    weights=Sum('weight'))

                if other_activity_groups['weights']:
                    if self.cleaned_data.get('weight') + other_activity_groups['weights'] > 100:
                        raise ValidationError({
                            'weight': ['The combined weight of activity groups in this output should not exceed 100.']})
            return self.cleaned_data
        except KeyError:
            raise ValidationError('error occured')


class ActivityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super(ActivityForm, self).__init__(*args, **kwargs)
        self.fields['form'].queryset = XForm.objects.all()
        self.fields['form'].label_from_instance = lambda obj: "%s" % (obj.title)
        try:
            self.fields['time_interval'].queryset = ProjectTimeInterval.objects.filter(project=self.instance.activity_group.project)
        except:
            self.fields['time_interval'].queryset = ProjectTimeInterval.objects.filter(project=project)

    class Meta:
        model = Activity
        fields = (
        'activity_group', 'name', 'description', 'beneficiary_level', 'target_number', 'target_unit', 'time_interval', 'form', 'weight')

        widgets = {
            'activity_group': forms.Select(attrs={'class': "custom-select"}),
            'name': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control'}),
            'target_number': forms.TextInput(attrs={'placeholder': 'Target Number', 'class': 'form-control'}),
            'target_unit': forms.TextInput(attrs={'placeholder': 'Target Unit', 'class': 'form-control'}),
            'time_interval': forms.Select(attrs={'class': "custom-select"}),
            'form': forms.Select(attrs={'class': "custom-select"}),
            'weight': forms.TextInput(attrs={'placeholder': 'Weight', 'class': 'form-control'})
        }

    def clean_weight(self):
        if not isinstance(self.cleaned_data.get('weight'), int) and not isinstance(self.cleaned_data.get('weight'),
                                                                                   float):
            raise ValidationError({'weight': ['Please enter a valid weight']})
        else:
            return self.cleaned_data.get('weight')

    def clean(self):
        cleaned_data = self.cleaned_data
        try:
            act_g = self.cleaned_data.get('activity_group')
            name = self.cleaned_data.get('name')
            description = self.cleaned_data.get('description')
            if not act_g == None:
                try:
                    a = Activity.objects.get(activity_group=act_g, name=name, description=description)
                    other_activities = Activity.objects.filter(activity_group=act_g).aggregate(
                        weights=Sum('weight'))
                    if other_activities.get('weight') is not None:
                        weights = other_activities.get('weights') - a.weight
                        if self.cleaned_data.get('weight') + weights > act_g.weight:
                            raise ValidationError({
                                'weight': [
                                    'The combined weight of activities in this activity group should not exceed the activity group weight.']})
                    else:
                        if self.cleaned_data.get('weight') > act_g.weight:
                            raise ValidationError({
                                'weight': [
                                    'The combined weight of activities in this activity group should not exceed the activity group weight.']})
                except Activity.DoesNotExist:
                    other_activities = Activity.objects.filter(activity_group=act_g).aggregate(
                        weights=Sum('weight'))
                    if other_activities.get('weight') is not None:
                        if self.cleaned_data.get('weight') + other_activities['weights'] > act_g.weight:
                            raise ValidationError({
                                'weight': [
                                    'The combined weight of activities in this activity group should not exceed the activity group weight.']})
                    else:
                        if self.cleaned_data.get('weight') > act_g.weight:
                            raise ValidationError({
                                'weight': [
                                    'The combined weight of activities in this activity group should not exceed the activity group weight.']})
                    return cleaned_data
        except KeyError:
            raise ValidationError('error occured')

    def save(self, commit=True):
        instance = super(ActivityForm, self).save(commit=False)
        if instance.beneficiary_level:
            instance.target_number = None
            instance.target_unit = None
        else:
            instance.target_number = self.cleaned_data.get('target_number')
            instance.target_unit = self.cleaned_data.get('target_unit')
        if commit:
            instance.save()
        return instance


class ClusterForm(forms.ModelForm):
    municipality = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Municipality.objects.all())

    class Meta:
        model = Cluster
        fields = ('name', 'municipality', 'ward', 'project')

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}),
            'ward': forms.TextInput(
                attrs={'placeholder': 'Wards for all municipalities(e.g., ward1, ward2)', 'class': 'form-control'}),
            'project': forms.Select(attrs={'class': "custom-select"}),
        }


class BeneficiaryForm(forms.ModelForm):
    class Meta:
        model = Beneficiary
        fields = (
        'name', 'address', 'ward_no', 'Type', 'GovernmentTranch', 'ConstructionPhase', 'Typesofhouse', 'Remarks',
        'cluster')

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

    def clean(self):
        cleaned_data = self.cleaned_data

        if cleaned_data.get('group').name == 'project-manager':
            if UserRole.objects.filter(group=cleaned_data.get('group'), project=cleaned_data.get('project')).exists():
                raise ValidationError({
                    'project': [
                        'A project can contain only a single project manager.'
                    ]
                })

        elif UserRole.objects.filter(group=cleaned_data.get('group'), cluster=cleaned_data.get('cluster')).exists():
            raise ValidationError({
                'cluster': [
                    'A cluster can contain only a single ' + str(cleaned_data.get('group'))]})

        if not self.instance.pk:
            if UserRole.objects.filter(
                    user=cleaned_data.get('user')).exists() and \
                    cleaned_data.get('group').name not in ['social-mobilizer', 'project-coordinator']:
                raise ValidationError({
                    'cluster': [
                        'This user has already been assigned to another cluster.']})
        return cleaned_data


class ConfigForm(forms.ModelForm):
    class Meta:
        model = Config
        fields = ('available_version', 'updates')


class ChangePasswordform(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    old_password = forms.CharField(widget=forms.PasswordInput, label='Your Old Password', max_length=100)
    new_password = forms.CharField(widget=forms.PasswordInput, label='Your New Password', max_length=100)
    confirm_new_password = forms.CharField(widget=forms.PasswordInput, label='One more time', max_length=100)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangePasswordform, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ChangePasswordform, self).clean()

        currentpassword = self.cleaned_data.get('user').password  # user's current password
        currentpasswordentered = self.cleaned_data.get("old_password")
        if not check_password(currentpasswordentered, currentpassword):
            raise ValidationError({'old_password': ['Your old password is incorrect!']})
        password = self.cleaned_data.get('new_password')
        password1 = self.cleaned_data.get('confirm_new_password')
        if password != password1:
            raise ValidationError({'new_password': ['The passwords did not match']})

        else:
            if password:
                if len(password) < 8:
                    raise ValidationError({'new_password': ['Passwords must be of more than 8 characters']})

                pattern = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$")
                if not bool(pattern.search(password)):
                    raise ValidationError(
                        {'new_password': ['Password must contain alphabet characters, special characters and numbers']})

    def save(self, commit=True):
        self.cleaned_data.get('user').set_password(self.cleaned_data['new_password'])
        if commit:
            self.cleaned_data.get('user').save()
        return self.cleaned_data.get('user')





