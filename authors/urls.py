from django.urls import path
from . import views

app_name = 'authors'

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path('register/create/', views.register_create, name='register_create'),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/recipe/new', views.dashboard_recipe_new, name='dashboard_recipe_new'),
    path('dashboard/recipe/delete', views.dashboard_recipe_delete, name='dashboard_recipe_delete'),
    path('dashboard/<int:pk>/edit', views.dashboard_recipe_edit, name='dashboard_recipe_edit'),
]