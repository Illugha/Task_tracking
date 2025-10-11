from django.urls import path
from task_tracking import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('task-create', views.TaskCreateView.as_view(), name='task-create'),
    path("<int:pk>/update/", views.TaskUpdateView.as_view(), name="task-update"),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),
    path('<int:pk>/complete/', views.TaskCompleteView.as_view(), name='task-complete'),
]

app_name = 'task_tracking'