from django.urls import path
from task_tracking import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task-list'),
]