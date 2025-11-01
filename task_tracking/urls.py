from django.urls import path
from task_tracking import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('task-create', views.TaskCreateView.as_view(), name='task-create'),
    path("<int:pk>/update/", views.TaskUpdateView.as_view(), name="task-update"),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),
    path('<int:pk>/complete/', views.TaskCompleteView.as_view(), name='task-complete'),
    path('delete-comment/<int:pk>/', views.CommentDeleteView.as_view(), name='comment-delete'),
    path('comment/like/<int:pk>/', views.CommentLikeToggle.as_view(), name='comment-like-toggle'),
    path('403/', views.custom_403_view.as_view(), name='custom-403'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
]

app_name = 'task_tracking'
