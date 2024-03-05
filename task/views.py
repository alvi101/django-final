from django.db.models.base import Model as Model
from django.shortcuts import render, redirect
from django.views.generic import DetailView, UpdateView, DeleteView, ListView, CreateView
from .models import Category, Task
from project.models import Project
from .forms import TaskForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Create your views here.


def send_account_email(mail_subject, template, title, to_email):
    message = render_to_string(template, {'title': title})
    send_email = EmailMultiAlternatives(mail_subject, '', to=[to_email])
    send_email.attach_alternative(message, 'text/html')
    send_email.send()


class Home(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(
            user=self.request.user.account)
        context["projects"] = Project.objects.filter(
            account=self.request.user.account)
        context["categories"] = Category.objects.all()
        return context


class AddTaskView(LoginRequiredMixin, FormView):
    form_class = TaskForm
    template_name = 'task/add_task.html'
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['account'] = self.request.user.account
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user.account
        form.instance.status = False
        title = form.cleaned_data['title']
        form.save()
        # send mail
        send_account_email(
            "Added new task", "email/add_task.html", title, self.request.user.email)
        return super().form_valid(form)


class AddCategoryView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'task/add_category.html'
    fields = ['name']


class EditTaskView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'due_date',
              'status', 'project', 'category']
    template_name = 'task/edit_task.html'
    success_url = reverse_lazy('home')


@login_required
def complete_task(request, pk):
    current_task = Task.objects.get(pk=pk)
    current_task.status = True
    current_task.save(update_fields=['status'])
    return redirect('home')


class DeleteTaskView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('home')
    template_name = 'task/delete_view.html'


class CategoryFilter(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'cat_filter.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projects"] = Project.objects.filter(
            account=self.request.user.account)
        context['categories'] = Category.objects.all()
        category = self.get_object()
        context['tasks'] = Task.objects.filter(
            user=self.request.user.account, category=category)
        return context


@login_required
def date_filter_earlist(request):
    tasks = Task.objects.filter(user=request.user.account).order_by('due_date')
    projects = Project.objects.filter(account=request.user.account)
    categories = Category.objects.all()
    context = {'tasks': tasks, 'projects': projects, 'categories': categories}
    return render(request, 'date_filtered.html', context)


@login_required
def date_filter_latest(request):
    tasks = Task.objects.filter(
        user=request.user.account).order_by('-due_date')
    projects = Project.objects.filter(account=request.user.account)
    categories = Category.objects.all()
    context = {'tasks': tasks, 'projects': projects, 'categories': categories}
    return render(request, 'date_latest.html', context)


@login_required
def status_completed(request):
    tasks = Task.objects.filter(
        status=True, user=request.user.account)
    projects = Project.objects.filter(account=request.user.account)
    categories = Category.objects.all()
    context = {'tasks': tasks, 'projects': projects, 'categories': categories}
    return render(request, 'date_latest.html', context)


@login_required
def status_not_completed(request):
    tasks = Task.objects.filter(
        status=False, user=request.user.account)
    projects = Project.objects.filter(account=request.user.account)
    categories = Category.objects.all()
    context = {'tasks': tasks, 'projects': projects, 'categories': categories}
    return render(request, 'date_latest.html', context)


class PriorityFilterView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'priority_filter.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = Task.objects.filter(
            user=self.request.user.account).order_by('-priority')
        context['projects'] = Project.objects.filter(
            account=self.request.user.account)
        context['categories'] = Category.objects.all()
        return context


class PriorityFilterReverse(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'priority_filter.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = Task.objects.filter(
            user=self.request.user.account).order_by('priority')
        context['projects'] = Project.objects.filter(
            account=self.request.user.account)
        context['categories'] = Category.objects.all()
        return context
