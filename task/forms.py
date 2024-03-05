from django import forms
from .models import Task, Category
from project.models import Project

"""
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    status = models.BooleanField()
    priority = models.CharField(
        max_length=2, choices=priority_levels, blank=True, null=True)

    # all related fields
    user = models.ForeignKey(UserAccount, related_name='account', on_delete=models.CASCADE)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='tasks', blank=True, null=True)
    category = models.ManyToManyField(Category, blank=True, related_name='tasks')
"""


class TaskForm(forms.ModelForm):
    def __init__(self, account, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # account = kwargs.pop('account')
        self.fields['project'].queryset = Project.objects.filter(
            account=account)

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date',
                  'priority', 'project', 'category',]
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }
