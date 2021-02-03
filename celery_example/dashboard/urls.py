from django.urls import path
from .views import PostScheduledListView, PostListView, PostDetailView, PostCreateView, PostStageListView, PostUpdateView, PostDeleteView, UserPostListView, PostScheduleListView
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='dashboard-home'),
    path('stage/', PostStageListView.as_view(), name='post-stage'),
    path('schedule/', PostScheduleListView.as_view(), name='post-schedule'),
    path('scheduled/', PostScheduledListView.as_view(), name='post-scheduled'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('about/', views.about, name='dashboard-about'),
]
