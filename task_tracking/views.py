from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Task
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from task_tracking.forms import TaskForm, TaskFilterForm
from task_tracking.mixins import UserIsOwnerMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

# List of existing tasks
class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')

        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskFilterForm(self.request.GET)
        return context

class TaskDetailView(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'tasks/task_detail.html'

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_tracking:task-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Task
    template_name = "tasks/task_update.html"
    form_class = TaskForm
    success_url = reverse_lazy("task_tracking:task-list")
    
class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixin, View):
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("task_tracking:task-list")

    def get_object(self):
        task_id = self.kwargs.get('pk')
        return get_object_or_404(Task, pk=task_id)

    def get(self, request, *args, **kwargs):
        task = self.get_object()
        return render(request, self.template_name, {'object': task})

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.delete()
        return redirect(self.success_url)

class TaskCompleteView(LoginRequiredMixin, UserIsOwnerMixin, View):
    def get_object(self):
        task_id = self.kwargs.get('pk')
        return get_object_or_404(Task, pk=task_id)

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.status = 'done'
        task.save()
        return HttpResponseRedirect(reverse_lazy('task_tracking:task-list'))
