from rest_framework.decorators import api_view  # type: ignore
from rest_framework.response import Response  # type: ignore
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer, TagSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status  # type: ignore
from tag.models import Tag


@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(Tag.objects.all(), pk=pk) # type: ignore
    serializer = TagSerializer(instance=tag, many=False,
                               context={'request': request})

    return Response(serializer.data)