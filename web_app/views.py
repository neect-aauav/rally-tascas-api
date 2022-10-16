from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(["GET"])
@csrf_exempt
def docs(request):
    return Response({
        "status": 404,
    }, status=status.HTTP_404_NOT_FOUND)

@api_view(["POST", "GET"])
@csrf_exempt
def signup(request):
    if request.method == "GET":
        return render(request, 'signup.html')
    
    if request.method == "POST":
        try:
            data = request.POST.dict()
            print(data)
            
        except ValueError:
            return Response({
                "status": 400,
                "message": "Invalid data format"
            }, status=status.HTTP_400_BAD_REQUEST)