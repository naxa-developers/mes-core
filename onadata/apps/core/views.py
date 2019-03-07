from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
# from django.conf.urls import reverse_lazy
from .models import Project, Output
from .forms import SignUpForm, ProjectForm


def logout_view(request):
    logout(request)

    return render()

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class HomeView(LoginRequiredMixin, TemplateView):
	template_name = 'core/index.html'


class SignInView(TemplateView):
	template_name = 'core/sign-in.html'


class SignUpView(TemplateView):
	template_name = 'core/sign-up.html'

	def signup(request):
		if request.method == 'POST':
			form = SignUpForm(request.POST)
			if form.is_valid():
				form.save()
				username = form.cleaned_data.get('username')
				raw_password = form.cleaned_data.get('password')
				user = authenticate(username=username, password=raw_password)
				login(request, user)
				return redirect('core/sign-in.html')

		else:
			form = SignUpForm()
		return render(request, 'core/sign-up.html', {'form': form})


class ProjectListView(ListView):
	model = Project
	template_name = 'core/project-list.html'

class ProjectDetailView(DetailView):
	model = Project
	template_name = 'core/project-detail.html' 


class ProjectCreateView(CreateView):
	model = Project
	template_name = 'core/project-form.html'
	form_class = ProjectForm
	success_url = reverse_lazy('project_list')


class ProjectUpdateView(UpdateView):
	model = Project
	template_name = 'core/project-form.html'
	form_class = ProjectForm
	success_url = reverse_lazy('project_list')


class ProjectDeleteView(DeleteView):
	model = Project
	template_name = 'core/project-delete.html'
	success_url = reverse_lazy('project_list')



class OutputListView(ListView):
	model = Output
	template_name = 'core/output-list.html'

		


