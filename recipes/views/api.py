from django.http import HttpResponse
from rest_framework.decorators import api_view  # type: ignore
from rest_framework.response import Response  # type: ignore

@api_view()
def recipe_api_list(request):
    return Response('ok')