
from django.urls import path
from .views import (
    BlogPostListView,
    BlogPostDetailView,
    BlogPostCreateView,
    BlogPostUpdateView,
    BlogPostDeleteView,
)

urlpatterns = [
    path('', BlogPostListView.as_view(), name='post_list'),  # Главная страница блога со списком постов
    path('post/<int:pk>/', BlogPostDetailView.as_view(), name='post_detail'),  # Детальная страница поста
    path('post/new/', BlogPostCreateView.as_view(), name='post_create'),  # Форма для создания нового поста
    path('post/<int:pk>/edit/', BlogPostUpdateView.as_view(), name='post_update'),  # Форма для редактирования поста
    path('post/<int:pk>/delete/', BlogPostDeleteView.as_view(), name='post_delete'),  # Подтверждение удаления поста
]
