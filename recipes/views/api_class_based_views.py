from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.views import APIView # type: ignore
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView # type: ignore
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from rest_framework.pagination import PageNumberPagination # type: ignore
from rest_framework.viewsets import ModelViewSet
from ..permissions import IsOwner
from django.shortcuts import get_object_or_404

class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 10

class RecipeAPIv2ViewSet(ModelViewSet):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'options', 'head', 'patch', 'delete', 'post']

    def get_object(self):
        pk = self.kwargs.get('pk', '')
        obj = get_object_or_404(self.queryset, pk=pk)

        self.check_object_permissions(self.request, obj)

        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE',]:
            return [IsOwner()]

        return super().get_permissions()

    def get_queryset(self):
        qs = super().get_queryset()

        return qs

class RecipeAPIv2List(ListCreateAPIView):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination

class RecipeAPIv2Detail(RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination