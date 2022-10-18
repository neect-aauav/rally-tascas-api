from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

import requests
import json

@api_view(["POST", "GET"])
@csrf_exempt
def signup(request):
    if request.method == "GET":
        return render(request, 'signup.html')
    
    if request.method == "POST":
        try:
            form_data = request.POST.dict()
            print(form_data)

            # make sure this is comming from the browser form
            if form_data["team-submit"] and form_data["team-submit"] == "Criar":
                data = {}
                data["team"] = form_data["team"]
                data["email"] = form_data["email"]

                other_fields = 3
                fields_per_member = 3
                number_members = int((len(form_data)-other_fields)/fields_per_member)
                members = []
                for i in range(0, number_members):
                    members.append({
                        "name": form_data[f"member[{i}]"],
                        "nmec": form_data[f"nmec[{i}]"],
                        "course": form_data[f"course[{i}]"]
                    })
                data["members"] = members

                requests.post(url="http://"+request.get_host()+"/api/teams", data=json.dumps(data))
                
                return render(request, 'signup.html')
        except ValueError as e:
            return Response({
                "status": 400,
                "message": "Invalid data format"
            }, status=status.HTTP_400_BAD_REQUEST)