import json
import requests

from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.models import MembersBars, Teams, Members, Bars, TeamsBars, Games, Prizes
from django.forms.models import model_to_dict

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
                game = Games.objects.get(id=data["game_id"])

                if len(data["members"]) > 0:
                    try:
                        members = [Members.objects.get(id=member["id"]) for member in data["members"]]
                    except Members.DoesNotExist as e:
                        response = {
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": f"There is no member with the given id"
                        }
                        logger.error(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]} ({e})')
                        return Response(response, status=response["status"])

                    # if the objects team, bar game and members exist, proceed to save the teamplay
                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Token {request.auth.key}"
                    }

                    # update team
                    requests.post(f"http://localhost:8000/api/teams/{data['team_id']}", json={
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

                    for member in members:
                        # update members
                        requests.post(f"http://localhost:8000/api/members/{member.id}", json={
                            "points": member.points + data["points"],
                            "drinks": member.drinks + data["drinks"],
                            "bar": {
                                "id": bar.id,
                                "points": data["points"],
                                "drinks": data["drinks"]
                            }
                        }, headers=headers)
                else:
                    response = {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "A team must have at least one member"
                    }
                    logger.error(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]}')
                    return Response(response, status=response["status"])
            except Teams.DoesNotExist as e:
                response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": f"There is no team with the id {data['team_id']}"
                }
                logger.error(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]} ({e})')
                return Response(response, status=response["status"])
            except Bars.DoesNotExist as e:
                response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": f"There is no bar with the id {data['bar_id']}"
                }
                logger.error(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]} ({e})')
                return Response(response, status=response["status"])
            except Games.DoesNotExist as e:
                response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": f"There is no game with the id {data['game_id']}"
                }
                logger.error(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]} ({e})')
                return Response(response, status=response["status"])
        except KeyError as e:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "JSON Keys missing"
            }
            logger.error(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]} ({e})')
            return Response(response, status=response["status"])
        except ValueError as e:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid JSON format"
            }
            logger.error(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]} ({e})')
            return Response(response, status=response["status"])