from django.urls import path
from authors.views import all as views
from authors.views import class_based_views as class_based_views

app_name = 'authors'

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path('register/create/', views.register_create, name='register_create'),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/recipe/new', class_based_views.DashboardRecipe.as_view(), name='dashboard_recipe_new'),
    path('dashboard/recipe/delete', class_based_views.DashboardRecipeDelete.as_view(), name='dashboard_recipe_delete'),
    path('dashboard/<int:pk>/edit', class_based_views.DashboardRecipe.as_view(), name='dashboard_recipe_edit'),
]