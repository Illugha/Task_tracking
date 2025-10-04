from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Task
from django.views.generic import ListView, DetailView, CreateView, View
from task_tracking.forms import TaskForm

# List of existing tasks
class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10

class TaskDetailView(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'tasks/task_detail.html'

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_tracking:task-list')