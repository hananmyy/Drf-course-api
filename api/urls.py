from django.urls import path
from . import views


urlpatterns = [
    path('products/', views.ProductListAPIView.as_view()), # use 'as.view() for class-based views
    path('products/info/', views.ProductInfoAPIView.as_view()),
    path('products/<int:product_id>/', views.ProductDetailAPIView.as_view()),
    path('orders/', views.OrderListAPIView.as_view()),
    path('user-orders/', views.UserOrderListAPIView.as_view(), name='user-orders'),
]
