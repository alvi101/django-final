from django.urls import path
from .views import FilterProject, AddProjectView, EditProjectView


urlpatterns = [
    path('filtered/<int:pk>/', FilterProject.as_view(), name='filter'),
    path('add-project/', AddProjectView.as_view(), name='add_project'),
    path('edit-project/<int:pk>/', EditProjectView.as_view(), name='edit_project'),
]
