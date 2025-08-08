from django.shortcuts import get_object_or_404
from rest_framework import status # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.views import APIView # type: ignore
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer

class RecipeAPIv2List(APIView):
    def get(self, request):
        recipes = Recipe.objects.get_published()[:10]
        serializer = RecipeSerializer(instance=recipes, many=True,
                                      context={'request': request})

        return Response(serializer.data)

    def post(self, request):
        serializer = RecipeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class RecipeAPIv2Detail(APIView):
    def get_recipe(self, pk):
        recipe = get_object_or_404(
            Recipe.objects.get_published(),
            pk=pk
        )

        return recipe

    def get(self, request, pk):
        recipe = self.get_recipe(pk)
        serializer = RecipeSerializer(instance=recipe, many=False,
                                      context={'request': request})

        return Response(serializer.data)

    def patch(self, request, pk):
        recipe = self.get_recipe(pk)
        serializer = RecipeSerializer(instance=recipe, data=request.data, many=False,
                                      context={'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, pk):
        recipe = self.get_recipe(pk)
        recipe.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)