from django.urls import path
from . import views

app_name = 'menu'
urlpatterns = [
    path(r'', views.menu_list, name='menu_list'),
    path(r'menu/<int:pk>/edit/', views.edit_menu, name='menu_edit'),
    path(r'menu/<int:pk>/', views.menu_detail, name='menu_detail'),
    path(r'menu/item/<int:pk>/', views.item_detail, name='item_detail'),
    path(
        r'menu/item/<int:pk>/edit/',
        views.edit_item,
        name='item_edit'),
    path(r'menu/new/', views.create_new_menu, name='menu_new'),
]
