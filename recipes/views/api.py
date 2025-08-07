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
        serializer = RecipeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response('Invalid request')

@api_view(['get', 'patch', 'delete',])
def recipe_api_detail(request, pk):
    recipe = get_object_or_404(
        Recipe.objects.get_published(),
        pk=pk
    )

    if request.method == 'GET':
        serializer = RecipeSerializer(instance=recipe, many=False,
                                      context={'request': request})

        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = RecipeSerializer(instance=recipe, data=request.data, many=False,
                                      context={'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    elif request.method == 'DELETE':
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response('Invalid request')

@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(Tag.objects.all(), pk=pk) # type: ignore
    serializer = TagSerializer(instance=tag, many=False,
                               context={'request': request})

    return Response(serializer.data)