import json
import requests

from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

from django.forms.models import model_to_dict

from api.models import MembersBars, Teams, Members, Bars, Games
from management import logger

@api_view(["POST"])
@permission_classes((IsAuthenticatedOrReadOnly,))
@csrf_exempt
def teamplay(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            try:
                team = Teams.objects.get(id=data["team_id"])
                bar = Bars.objects.get(id=data["bar_id"])
                game = Games.objects.get(id=bar.game.id)

                if len(data["members"]) > 0:
                    
                    # verify if points from team match points from members
                    members_points = [member["points"] for member in data["members"]]
                    if sum(members_points) != data["points"]:
                        response = {
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": "Points from team and members don't match"
                        }
                        logger.error(request.auth.key, f'[{response["status"]}]@"{request.method} {request.path}": {response["message"]}')
                        return Response(response, status=response["status"])

                    # if the objects team, bar game and members exist, proceed to save the teamplay
                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Token {request.auth.key}"
                    }

                    # update team
                    requests.patch(f"http://localhost:8000/api/teams/{data['team_id']}", json={
                        "points": team.points + data["points"],
                        "drinks": team.drinks + data["drinks"],
                        "has_egg": data["has_egg"],
                        "puked": team.puked + data["puked"],
                        "bar": {
                            "id": bar.id,
                            "points": data["points"],
                            "drinks": data["drinks"],
                            "has_egg": data["has_egg"],
                            "puked": data["puked"],
                            "won_game": data["game_completed"]
                        }
                    }, headers=headers)

                    try:
                        for member in data["members"]:
                            member_object = Members.objects.get(id=member["id"])
                            # update members
                            requests.patch(f"http://localhost:8000/api/members/{member['id']}", json={
                                "points": member_object.points + member["points"],
                                "drinks": member_object.drinks + member["drinks"],
                                "bar": {
                                    "id": bar.id,
                                    "points": member["points"],
                                    "drinks": member["drinks"]
                                }
                            }, headers=headers)
                    except Members.DoesNotExist as e:
                        response = {
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": f"There is no member with the given id"
                        }
                        logger.error(request.auth.key, f'[{response["status"]}]@"{request.method} {request.path}": {response["message"]} ({e})')
                        return Response(response, status=response["status"])

                    # update bars
                    requests.patch(f"http://localhost:8000/api/bars/{data['bar_id']}", json={
                        "points": bar.points + data["points"],
                        "drinks": bar.drinks + data["drinks"],
                        "puked": bar.puked + data["puked"],
                    }, headers=headers)

                    # update games
                    requests.patch(f"http://localhost:8000/api/games/{game.id}", json={
                        "completed": game.completed + 1 if data["game_completed"] else 0
                    }, headers=headers)

                    response = {
                        "status": status.HTTP_200_OK,
                        "message": f"Teamplay successfully saved"
                    }
                    logger.info(request.auth.key, f'[{response["status"]}]@"{request.method} {request.path}": {response["message"]}')
                    return Response(response, status=response["status"])
                else:
                    response = {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "A team must have at least one member"
                    }
                    logger.error(request.auth.key, f'[{response["status"]}]@"{request.method} {request.path}": {response["message"]}')
                    return Response(response, status=response["status"])
            except Teams.DoesNotExist as e:
                response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": f"There is no team with the id {data['team_id']}"
                }
                logger.error(request.auth.key, f'[{response["status"]}]@"{request.method} {request.path}": {response["message"]} ({e})')
                return Response(response, status=response["status"])
            except Bars.DoesNotExist as e:
                response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": f"There is no bar with the id {data['bar_id']}"
                }
                logger.error(request.auth.key, f'[{response["status"]}]@"{request.method} {request.path}": {response["message"]} ({e})')
                return Response(response, status=response["status"])
            except Games.DoesNotExist as e:
                response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": f"That bar doesn't have a game"
                }
                logger.error(request.auth.key, f'[{response["status"]}]@"{request.method} {request.path}": {response["message"]} ({e})')
                return Response(response, status=response["status"])
        except KeyError as e:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "JSON Keys missing"
            }
            logger.error(request.auth.key, f'[{response["status"]}]@"{request.method} {request.path}": {response["message"]} ({e})')
            return Response(response, status=response["status"])
        except ValueError as e:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid JSON format"
            }
            logger.error(request.auth.key, f'[{response["status"]}]@"{request.method} {request.path}": {response["message"]} ({e})')
            return Response(response, status=response["status"])

        
@api_view(['GET'])
@permission_classes((AllowAny,))
@csrf_exempt
def scoreboard_teams(request):
    if request.method == "GET":
        try:
            teams = Teams.objects.all().order_by('-points')
            
            # iterate all teams
            scoreboard = [[team.name, team.points, team.drinks] for team in teams]

            logger.info(request.auth.key, f'[{status.HTTP_200_OK}]@"{request.method} {request.path}": Teams scoreboard successfully retrieved')
            return Response(scoreboard, status=status.HTTP_200_OK)
        except Teams.DoesNotExist as e:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "There are no teams"
            }
            logger.error(request.auth.key, f'[{response["status"]}]@"{request.method} {request.path}": {response["message"]} ({e})')
            return Response(response, status=response["status"])


@api_view(['GET'])
@permission_classes((AllowAny,))
@csrf_exempt
def scoreboard_members(request, team=None):
    if request.method == "GET":
        try:
            scoreboard = []

            if team and team != "all":
                members = Members.objects.filter(team=team).order_by('-points')
                for member in members:
                    member_score = [member.name]

                    # get bars from this member
                    member_score += [model_to_dict(row)['points'] for row in MembersBars.objects.filter(memberId=member.id)]

                    member_score.append(member.points)

                    scoreboard.append(member_score)
            elif team == "all":
                members = Members.objects.all().order_by('-points')

                all_teams = Teams.objects.all()
                for team in all_teams:
                    members_score = []
                    members_team = members.filter(team=team.id)
                    for member in members_team:
                        member_score = [member.name]

                        # get bars from this member
                        member_score += [model_to_dict(row)['points'] for row in MembersBars.objects.filter(memberId=member.id)]

                        member_score.append(member.points)

                        members_score.append(member_score)

                    scoreboard.append({
                        "team": team.name,
                        "members": members_score
                    })
            else:
                members = Members.objects.all().order_by('-points')

                for member in members:
                    member_score = [member.name]

                    # get bars from this member
                    member_score += [model_to_dict(row)['points'] for row in MembersBars.objects.filter(memberId=member.id)]

                    member_score.append(member.points)

                    scoreboard.append(member_score)

            logger.info(request.auth.key, f'[{status.HTTP_200_OK}]@"{request.method} {request.path}": Members scoreboard successfully retrieved')
            return Response(scoreboard, status=status.HTTP_200_OK)
        except Members.DoesNotExist as e:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "There are no members"
            }
            logger.error(request.auth.key, f'[{response["status"]}]@"{request.method} {request.path}": {response["message"]} ({e})')
            return Response(response, status=response["status"])