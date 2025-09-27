from django.shortcuts import render
from .models import Task
from django.views.generic import ListView, DetailView, CreateView, View

# List of existing tasks
class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10
