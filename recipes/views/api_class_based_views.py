from django.shortcuts import get_object_or_404
from rest_framework import status # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.views import APIView # type: ignore
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView # type: ignore
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from rest_framework.pagination import PageNumberPagination # type: ignore

class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 10

class RecipeAPIv2List(ListCreateAPIView):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination

class RecipeAPIv2Detail(RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination