# from django.shortcuts import render

# from django.http import HttpResponse

# def home(request):
#     return HttpResponse("Hello from Blog Home!")

# def post_detail(request, post_id):
#     return HttpResponse(f"Post ID: {post_id}")


from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_home(request):
    return Response({"message": "Hello from Django API!"})