from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from task_tracking.models import Task, Comment  
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from task_tracking.forms import TaskForm, TaskFilterForm, CommentForm, UserLoginForm, UserRegistrationForm
from task_tracking.mixins import UserIsOwnerMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from task_tracking import models


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.task = self.get_object()
            comment.save()
            return redirect('task_tracking:task-detail', pk=comment.task.pk)
        else:
            pass

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
    
class CommentDeleteView(LoginRequiredMixin, View):
    template_name = "tasks/comment_confirm_delete.html"

    def get_object(self):
        comment_id = self.kwargs.get('pk')
        return get_object_or_404(Comment, pk=comment_id, author=self.request.user)

    def get(self, request, *args, **kwargs):
        comment = self.get_object()
        return render(request, self.template_name, {'object': comment})

    def post(self, request, *args, **kwargs):
        comment = self.get_object()
        task_id = comment.task.pk
        comment.delete()
        return redirect('task_tracking:task-detail', pk=task_id)


class custom_403_view(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tasks/403.html', status=403)

class CustomLoginView(View):
    template_name = 'tasks/login.html'
    form_class = UserLoginForm

class CustomLoginView(LoginView):
    template_name = 'tasks/login.html'
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    next_page = "task_tracking:login"

class RegisterView(CreateView):
    template_name = 'tasks/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('task_tracking:login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)

class CommentLikeToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(models.Comment, pk=self.kwargs.get('pk'))
        like_qs = models.Like.objects.filter(comment=comment, user=request.user)
        if like_qs.exists():
            like_qs.delete()
        else:
            models.Like.objects.create(comment=comment, user=request.user)
        return HttpResponseRedirect(comment.get_absolute_url())