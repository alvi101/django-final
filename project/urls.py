from django.urls import path
from .views import FilterProject, AddProjectView


urlpatterns = [
    path('filtered/<int:pk>/', FilterProject.as_view(), name='filter'),
    path('add-project/', AddProjectView.as_view(), name='add_project'),
]
