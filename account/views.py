from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegistrationForm
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from task.models import Task, Category
from project.models import Project
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
# Create your views here.


def send_account_email(mail_subject, template, user, to_email):
    message = render_to_string(template, {'user': user})
    send_email = EmailMultiAlternatives(mail_subject, '', to=[to_email])
    send_email.attach_alternative(message, 'text/html')
    send_email.send()


class Home(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 'tasks'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = Task.objects.filter(user=self.request.user.account)
        context["projects"] = Project.objects.filter(account=self.request.user.account)
        context["categories"] = Category.objects.all
        return context
    


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        username = form.cleaned_data['username']
        send_account_email(
            "Welcome to TaskMaster", "email/registration_mail.html", username, email)
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    model = Task
    template_name = 'account/profile.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(user=self.request.user.account)
        context['projects'] = Project.objects.filter(
            account=self.request.user.account)
        context['categories'] = Category.objects.all()
        return context


class UserLogin(LoginView):
    template_name = 'account/login.html'
    success_url = reverse_lazy('home')
