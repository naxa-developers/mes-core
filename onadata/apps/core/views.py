from django.views.generic import TemplateView

class HomeView(TemplateView):
	template_name = 'core/index.html'


class ProjectListView(TemplateView):
	template_name = 'core/project-list.html'


class SignInView(TemplateView):
	template_name = 'core/sign-in.html'


class SignUpView(TemplateView):
	template_name = 'core/sign-up.html'