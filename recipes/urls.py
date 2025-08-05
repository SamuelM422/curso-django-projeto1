from django.urls import path
import recipes.views.class_based_views as class_based_views
import recipes.views.theory as theory_view
import recipes.views.api as api_view

app_name = 'recipes'

urlpatterns = [
    path("", class_based_views.RecipeListViewHome.as_view(), name="home"),
    path('recipes/search/', class_based_views.RecipeListViewSearch.as_view(), name='search'),
    path('recipes/category/<int:category_id>/', class_based_views.RecipeListViewCategory.as_view(), name='category'),
    path("recipes/<int:pk>/", class_based_views.RecipeDetailView.as_view(), name="recipe"),
    path('recipes/api/v1/', class_based_views.RecipeListViewApi.as_view(), name='recipes_api_v1'),
    path('recipes/api/v1/<int:pk>/', class_based_views.RecipeDetailApi.as_view(), name='recipes_api_v1_detail'),
    path('recipes/theory', theory_view.theory, name='theory'),
    path('recipes/tags/<slug:slug>/', class_based_views.RecipeListViewTag.as_view(), name='tags'),
    path('recipes/api/v2/', api_view.recipe_api_list, name='recipes_api_v2'),
    path('recipes/api/v2/<int:pk>/', api_view.recipe_api_detail, name='recipes_api_v2_detail')
]
