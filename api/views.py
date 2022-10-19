from cmath import isnan
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.models import Teams, Members, Bars, TeamsBars
from django.forms.models import model_to_dict

from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import *

from neectrally.settings import BASE_DIR

import json
import qrcode
import random

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
                        try:
                            team_object = Teams(name=data['team'], email=data['email'])
                            team_object.save()

                            # loop through members
                            for member in data['members']:
                                member_object = Members(name=member['name'], course=member['course'], nmec=member['nmec'], team=team)
                                member_object.save()


                            # qr code generation
                            qr_name = f'qr_team{team_object.id}.png'
                            path = f'{BASE_DIR}/static/{qr_name}'

                            l = [RadialGradiantColorMask(), SquareGradiantColorMask(), HorizontalGradiantColorMask(), VerticalGradiantColorMask()]
                            
                            qr = qrcode.QRCode(
                                version=1,
                                error_correction=qrcode.constants.ERROR_CORRECT_L,
                                border=2
                            )
                            qr.add_data('http://127.0.0.1:8000/api/docs/')

                            img = qr.make_image(image_factory=StyledPilImage, color_mask=l[random.randint(0,3)])
                            img.save(path)

                            team_object.qr_code = qr_name
                            team_object.save()
                            
                            return Response({
                                "status": 200,
                                "message": f"Added team {data['team']} successfully"
                            }, status=status.HTTP_200_OK)
                        except Exception as e:
                            # team_object.delete()

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
        except ValueError as e:
            return Response({
                "status": 400,
                "message": "Invalid JSON format",
                "error": str(e)
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
                    team_objects = [Teams.objects.get(name=request.GET.get("name"))]
                elif request.GET.get("ePOSTmail"):
                    team_objects = [Teams.objects.get(email=request.GET.get("email"))]
                elif request.GET.get("id"):
                    team_objects = [Teams.objects.get(id=request.GET.get("id"))]
                else:
                    # return all teams
                    team_objects = Teams.objects.all()

                teams = []
                for team_object in team_objects:
                    team = model_to_dict(team_object)

                    # get members from this team
                    team["members"] = [model_to_dict(member) for member in Members.objects.filter(team=team['id'])]
                    teams.append(team)

                return Response(teams[0] if len(teams) == 1 else teams, status=status.HTTP_200_OK)
            except Teams.DoesNotExist:
                return Response({
                    "status": 400,
                    "message": f"There is no team with that identification"
                }, status=status.HTTP_400_BAD_REQUEST) 

    if request.method == "DELETE":
        if id is not None:
            try:
                team= Teams.objects.get(id=id)
                team.delete()

                return Response({
                    "status": 200,
                    "message": f"Deleted team {team.name}"
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
        
@api_view(["POST", "GET", "DELETE"])
@csrf_exempt
def bars(request, id=None):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            try:
                try:
                    Bars.objects.get(name=data["name"])

                    # if already exists, break
                    return Response({
                        "status": 400,
                        "message": f"A bar with the name {data['name']} already exists"
                    }, status=status.HTTP_400_BAD_REQUEST)
                except Bars.DoesNotExist:
                    bar = Bars(name=data['name'], location=data['location'], picture=data['picture'])

                    try:
                        bar.save()

                        # fill TeamsBars
                        all_teams = Teams.objects.all()
                        for team in all_teams:
                            # check if the assoc already exists
                            try:
                                TeamsBars.objects.get(barId=bar, teamId=team)
                            except TeamsBars.DoesNotExist:
                                team_bars_assoc = TeamsBars(teamId=team, barId=bar)                        
                                team_bars_assoc.save()

                        return Response({
                            "status": 200,
                            "message": f"Added bar {data['name']} successfully"
                        }, status=status.HTTP_200_OK)
                    except Exception:
                        bar.delete()

                        return Response({
                            "status": 500,
                            "message": f"Could not add bar {data['name']}"
                        },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
                bar_object = Bars.objects.get(id=id)
                bar = model_to_dict(bar_object)

                return Response(bar, status=status.HTTP_200_OK) 
            except Bars.DoesNotExist:
                return Response({
                    "status": 400,
                    "message": f"There is no bar with the id {id}"
                }, status=status.HTTP_400_BAD_REQUEST) 
        else:
            # check for other ways of team identification
            try:
                if request.GET.get("name"):
                    bar_objects = [Bars.objects.get(name=request.GET.get("name"))]
                elif request.GET.get("email"):
                    bar_objects = [Bars.objects.get(email=request.GET.get("email"))]
                elif request.GET.get("id"):
                    bar_objects = [Bars.objects.get(id=request.GET.get("id"))]
                else:
                    # return all teams
                    bar_objects = Bars.objects.all()

                bars = []
                for bar_object in bar_objects:
                    bar = model_to_dict(bar_object)
                    bars.append(bar)

                return Response(bars[0] if len(bars) == 1 else bars, status=status.HTTP_200_OK)
            except Teams.DoesNotExist:
                return Response({
                    "status": 400,
                    "message": f"There is no bar with that identification"
                }, status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == "DELETE":
        if id is not None:
            try:
                bar = Bars.objects.get(id=id)
                bar.delete()

                return Response({
                    "status": 200,
                    "message": f"Deleted bar {bar.name}"
                }, status=status.HTTP_200_OK) 
            except Bars.DoesNotExist:
                return Response({
                    "status": 400,
                    "message": f"There is no bar with the id {id}"
                }, status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response({
                "status": 400,
                "message": "Missing bar identifier"
            }, status=status.HTTP_400_BAD_REQUEST) 


@api_view(["POST", "GET"])
@csrf_exempt
def points(request, id=None, method=None):
    if request.method == "POST":
        if id is not None:
            try:
                float(id)
            except ValueError:
                return Response({
                    "status": 400,
                    "message": "Team id must be a number"
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                data = json.loads(request.body)
                try:
                    try:
                        points = float(data["points"])
                    except ValueError:
                        return Response({
                            "status": 400,
                            "message": "Points must be a number"
                        }, status=status.HTTP_400_BAD_REQUEST)

                    try:
                        team = Teams.objects.get(id=id)
                        members = Members.objects.filter(team=team)

                        if method is None:
                            method = "set"

                        # handle teams points
                        old_points = team.points
                        team.points = _operate_points(team.points, points, method)

                        # handle members points
                        not_handled = _handle_points(data, members, method)
                        if not_handled is not None:
                            return not_handled

                        # association team <-> bar
                        try:
                            bar = Bars.objects.get(id=data["bar"])
                            team_bar_assoc = TeamsBars.objects.get(teamId=team, barId=bar)
                            team_bar_assoc.points = _operate_points(team_bar_assoc.points, team.points, method)
                            team_bar_assoc.save()
                        except Bars.DoesNotExist:
                            return Response({
                                "status": 400,
                                "message": f"A bar with the id {data['bar']} doesn't exist"
                            },status=status.HTTP_400_BAD_REQUEST)

                        team.save()

                        if method == "add":
                            message = f"Added {points} points to team {team.name}. Team's ballance went from {old_points} to {team.points}"
                        if method == "remove":
                            message = f"Removed {points} points from team {team.name}. Team's ballance went from {old_points} to {team.points}"
                        if method == "set":
                            message = f"Set points of team {team.name} from {old_points} to {team.points}"

                        return Response({
                            "status": 200,
                            "message": f"{bar.name}: {message}",
                            "points": team.points
                        }, status=status.HTTP_200_OK)

                    except Teams.DoesNotExist:
                        return Response({
                            "status": 400,
                            "message": f"A team with the id {id} doesn't exist"
                        },status=status.HTTP_400_BAD_REQUEST)

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
        else:
            return Response({
                "status": 400,
                "message": "Missing team ID"
            }, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        if id is not None:
            try:
                float(id)
            except ValueError:
                return Response({
                    "status": 400,
                    "message": "Team id must be a number"
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                team = Teams.objects.get(id=id)
                return Response({"points": team.points}, status=status.HTTP_200_OK)

            except Teams.DoesNotExist:
                return Response({
                    "status": 400,
                    "message": f"A team with the id {id} doesn't exist"
                },status=status.HTTP_400_BAD_REQUEST)


def _handle_points(data, members, method):
        if "members" in data:
            # check if points of each member matches overall points
            try:
                members_points = sum([float(member["points"]) for member in data["members"]])
                if members_points != data["points"]:
                    return Response({
                        "status": 400,
                        "message": "Number of overall points must be the same of all the points from members"
                    }, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({
                    "status": 400,
                    "message": "Member points must be a number"
                }, status=status.HTTP_400_BAD_REQUEST)

            not_distributed = _distribute_points(data["members"], method)
            if not_distributed is not None:
                return not_distributed
        else:
            # split points equally
            for member in members:
                member.points = _operate_points(member.points, data["points"]/len(members), method)
                member.save()

def _distribute_points(members, method):
    for member_id in members:
        if "id" in member_id:
            member = Members.objects.get(id=id["id"])
        elif "nmec" in member_id:
            member = Members.objects.get(nmec=member_id["nmec"])
        else:
            return Response({
                "status": 400,
                "message": "Missing valid member identification"
            },status=status.HTTP_400_BAD_REQUEST)
        
        try:
            member_points = float(member_id["points"])
        except ValueError:
            return Response({
                "status": 400,
                "message": "Member points must be a number"
            }, status=status.HTTP_400_BAD_REQUEST)

        member.points = _operate_points(member.points, member_points, method)
        member.save()

def _operate_points(points, value, method):
        if method == "add":
            points += value
        elif method == "remove":
            points -= value
        elif method == "set":
            points = value
        else:
            points = points

        return points