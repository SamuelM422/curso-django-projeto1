from collections import defaultdict
from authors.validators import AuthorRecipeValidator
from rest_framework import serializers  # type: ignore
from recipes.models import Category, Recipe
from django.contrib.auth import get_user_model

from tag.models import Tag

User = get_user_model()

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

class RecipeSerializer(serializers.Serializer):
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'author', 'category', 'tags', 'public', 'preparation', 'tag_objects',
            'tag_links', 'preparation_time', 'preparation_time_unit', 'servings', 'servings_unit', 'preparation_steps',
            'cover'
        ]

    public = serializers.BooleanField(source='is_published', read_only=True)
    preparation = serializers.SerializerMethodField(method_name='get_preparation_method', read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )
    category_name = serializers.StringRelatedField(source='category')
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    tags_objects = TagSerializer(
        many=True,
        source='tags',
    )
    tags_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        queryset=Tag.objects.all(),
        view_name='recipes:recipes_api_v2_tag',
    )

    @staticmethod
    def get_preparation_method(recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'

    def validate(self, attrs):
        if self.instance is not None and attrs.get('servings') is None:
            attrs['servings'] = self.instance.servings

        if self.instance is not None and attrs.get('preparation_time') is None:
            attrs['preparation_time'] = self.instance.preparation_time

        super_validate = super().validate(attrs)

        AuthorRecipeValidator(attrs, error_class=serializers.ValidationError)

        return super_validate