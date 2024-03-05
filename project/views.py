from django.shortcuts import render
from django.views.generic import DetailView, CreateView
from .models import Project
from task.models import Category, Task
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProjectForm

# Create your views here.


class AddProjectView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/add_project.html'
    success_url = reverse_lazy('home')


    def form_valid(self, form):
        form.instance.account = self.request.user.account
        form.save()
        return super().form_valid(form)


class FilterProject(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'filtered.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["tasks"] = Task.objects.filter(user=self.request.user.account)
        context["projects"] = Project.objects.filter(account=self.request.user.account)
        return context
