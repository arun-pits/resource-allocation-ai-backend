from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello from Blog Home!")

# def post_detail(request, post_id):
#     return HttpResponse(f"Post ID: {post_id}")
