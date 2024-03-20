from django.urls import path
from .views import (
    CategoryFilter,
    date_filter_earlist,
    date_filter_latest,
    AddTaskView,
    EditTaskView,
    DeleteTaskView,
    complete_task,
    PriorityFilterView,
    PriorityFilterReverse,
    AddCategoryView,
    status_completed,
    status_not_completed,
)

urlpatterns = [
    path('category/filter/<int:pk>/', CategoryFilter.as_view(), name='cat_filter'),
    path('date/filter/earliest/', date_filter_earlist, name='filter_earliest'),
    path('status/filter/completed/', status_completed, name='completed'),
    path('status/filter/not-completed/',
         status_not_completed, name='not_completed'),
    path('date/filter/latest/', date_filter_latest, name='filter_latest'),
    path('add/task/', AddTaskView.as_view(), name='add_task'),
    path('add/category/', AddCategoryView.as_view(), name='add_category'),
    path('edit/task/<int:pk>/', EditTaskView.as_view(), name='edit_task'),
    path('delete/task/<int:pk>/', DeleteTaskView.as_view(), name='delete_task'),
    path('status/task/<int:pk>/', complete_task, name='edit_status'),
    path('priority-high/task/', PriorityFilterView.as_view(), name='priority_high'),
    path('priority-low/task/', PriorityFilterReverse.as_view(), name='priority_low'),
]
