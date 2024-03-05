from django.db import models
from account.models import UserAccount
from project.models import Project
from .constants import priority_levels

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    status = models.BooleanField()
    priority = models.CharField(
        max_length=2, choices=priority_levels, blank=True, null=True)

    # all related fields
    user = models.ForeignKey(
        UserAccount, related_name='account', on_delete=models.CASCADE)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='tasks', blank=True, null=True)
    category = models.ManyToManyField(
        Category, blank=True, related_name='tasks')

    def __str__(self):
        return f'{self.title}'
