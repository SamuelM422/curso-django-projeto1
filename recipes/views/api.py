from rest_framework.decorators import api_view  # type: ignore
from rest_framework.response import Response  # type: ignore
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer, TagSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status  # type: ignore
from tag.models import Tag


@api_view(['get', 'post'])
def recipe_api_list(request):
    if request.method == 'GET':
        recipes = Recipe.objects.get_published()[:10]
        serializer = RecipeSerializer(instance=recipes, many=True,
                                      context={'request': request})

        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RecipeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
    else:
        return Response('Invalid request')

@api_view()
def recipe_api_detail(request, pk):
    recipes = get_object_or_404(
        Recipe.objects.get_published(),
        pk=pk
    )
    serializer = RecipeSerializer(instance=recipes, many=False,
                                  context={'request': request})

    return Response(serializer.data)

@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(Tag.objects.all(), pk=pk) # type: ignore
    serializer = TagSerializer(instance=tag, many=False,
                               context={'request': request})

    return Response(serializer.data)