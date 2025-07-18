from django.contrib import admin
from .models import Category, Recipe, Authors

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    pass

class RecipeAdmin(admin.ModelAdmin):
    pass

class AuthorsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Authors, AuthorsAdmin)