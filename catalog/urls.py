from django.urls import path
from .views import (
    HomeView, ContactView, IndexView,
    ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView,
    ProductUpdateView
)

urlpatterns = [
    # Основные страницы
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('index/', IndexView.as_view(), name='index'),

    # Продукты (CRUD)
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('products/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('category/<int:category_id>/products/', views.ProductsByCategoryView.as_view(), name='products_by_category'),

]
