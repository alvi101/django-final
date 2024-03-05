from django.db import models
from account.models import UserAccount

# Create your models here.


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()

    # all related fields
    account = models.ForeignKey(UserAccount, related_name='project', on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.title}'