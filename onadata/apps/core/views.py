from django.views.generic import TemplateView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm

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


class ProjectListView(TemplateView):
	template_name = 'core/project-list.html'


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