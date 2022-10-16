from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

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