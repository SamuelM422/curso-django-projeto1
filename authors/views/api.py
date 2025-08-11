from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from ..serializers import AuthorSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

class AuthorViewSet(ReadOnlyModelViewSet):
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = get_user_model()
        qs = user.objects.filter(username=self.request.user.username)

        return qs

    @action(detail=False, methods=['get'])
    def me(self):
        obj = self.get_queryset()
        serializer = self.get_serializer(
            instance=obj,
        )

        return Response(serializer.data)