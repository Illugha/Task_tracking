from django.urls import path
from task_tracking import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('task-create', views.TaskCreateView.as_view(), name='task-create'),
    path("<int:pk>/update/", views.TaskUpdateView.as_view(), name="task-update"),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),
    path('<int:pk>/complete/', views.TaskCompleteView.as_view(), name='task-complete'),
    path('<int:pk>/comment/', views.CommentCreateView.as_view(), name='task-comment'),
    path('delete-comment/<int:pk>/', views.CommentDeleteView.as_view(), name='comment-delete'),
    path('403/', views.custom_403_view.as_view(), name='custom-403'),
]

app_name = 'task_tracking'