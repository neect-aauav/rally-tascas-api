from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import RegistrationSerializer

@api_view(["POST", "GET"])
@csrf_exempt
def register(request):
    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            return Response({
                "status": 200,
                "message": f"Successfully registered admin user {account.username}"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": 400,
                "message": "Something went wrong... Could not create admin user"
            }, status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == "GET":
        return render(request, 'register.html')

@api_view(["POST", "GET"])
@csrf_exempt
def login(request):
    if request.method == "GET":
        return render(request, 'admin.html')
    
    if request.method == "POST":
        try:
            data = request.POST.dict()
            print(data)
            
        except ValueError:
            return Response({
                "status": 400,
                "message": "Invalid data format"
            }, status=status.HTTP_400_BAD_REQUEST)