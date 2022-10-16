from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.models import Teams, Members
from django.forms.models import model_to_dict

import json

@api_view(["POST", "GET", "DELETE"])
@csrf_exempt
def teams(request, id=None):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            try:
                if len(data["members"]) > 0:
                    print(data)

                    try:
                        Teams.objects.get(name=data["team"])

                        # if already exists, break
                        return Response({
                            "status": 400,
                            "message": f"A team with the name {data['team']} already exists"
                        }, status=status.HTTP_400_BAD_REQUEST)
                    except Teams.DoesNotExist:
                        team_object = Teams(name=data['team'], email=data['email'])
                        try:
                            team_object.save()

                            # loop through members
                            for member in data['members']:
                                print(member)
                                member_object = Members(name=member['name'], course=member['course'], nmec=member['nmec'], team=team_object)
                                member_object.save()

                            return Response({
                                "status": 200,
                                "message": f"Added team {data['team']} successfully"
                            }, status=status.HTTP_200_OK)
                        except Exception as e:
                            team_object.delete()

                            return Response({
                                "status": 500,
                                "message": f"Could not add team {data['team']}",
                                "error": str(e)
                            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({
                        "status": 400,
                        "message": "Number of members can't be 0"
                    }, status=status.HTTP_400_BAD_REQUEST)
            except KeyError:
                return Response({
                    "status": 400,
                    "message": "JSON Keys missing"
                }, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({
                "status": 400,
                "message": "Invalid JSON format"
            }, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == "GET":
        if id is not None:
            try:
                team_object = Teams.objects.get(id=id)
                team = model_to_dict(team_object)

                # get members from this team
                team["members"] = [model_to_dict(member) for member in Members.objects.filter(team=id)]

                return Response(team, status=status.HTTP_200_OK) 
            except Teams.DoesNotExist:
                return Response({
                    "status": 400,
                    "message": f"There is no team with the id {id}"
                }, status=status.HTTP_400_BAD_REQUEST) 
        else:
            # check for other ways of team identification
            try:
                if request.GET.get("name"):
                    team_object = Teams.objects.get(name=request.GET.get("name"))
                elif request.GET.get("email"):
                    team_object = Teams.objects.get(email=request.GET.get("email"))
                elif request.GET.get("id"):
                    team_object = Teams.objects.get(id=request.GET.get("id"))
                else:
                    return Response({
                        "status": 400,
                        "message": f"Missing team identifier"
                    }, status=status.HTTP_400_BAD_REQUEST)

                team = model_to_dict(team_object)

                # get members from this team
                team["members"] = [model_to_dict(member) for member in Members.objects.filter(team=team['id'])]

                return Response(team, status=status.HTTP_200_OK)
            except Teams.DoesNotExist:
                return Response({
                    "status": 400,
                    "message": f"There is no team with that identification"
                }, status=status.HTTP_400_BAD_REQUEST) 

    if request.method == "DELETE":
        if id is not None:
            try:
                team_object = Teams.objects.get(id=id)
                team = model_to_dict(team_object)
                team_object.delete()

                return Response({
                    "status": 200,
                    "message": f"Deleted team {team['name']}"
                }, status=status.HTTP_200_OK) 
            except Teams.DoesNotExist:
                return Response({
                    "status": 400,
                    "message": f"There is no team with the id {id}"
                }, status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response({
                "status": 400,
                "message": "Missing team identifier"
            }, status=status.HTTP_400_BAD_REQUEST) 