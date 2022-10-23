from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.models import MembersBars, Teams, Members, Bars, TeamsBars, Games, Prizes
from django.forms.models import model_to_dict

from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import *

from neectrally.settings import BASE_DIR
from management import logger

import json
import qrcode
import random
import os
import requests

@api_view(["GET", "POST", "DELETE", "PATCH"])
@permission_classes((IsAuthenticatedOrReadOnly,))
@csrf_exempt
def teams(request, id=None):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            try:
                if len(data["members"]) > 0:
                    try:
                        Teams.objects.get(name=data["team"])

                        response = {
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": f"A team with the name {data['team']} already exists"
                        }
                        logger.error(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]}')
                        return Response(response, status=response["status"])
                    except Teams.DoesNotExist:
                        try:
                            team = Teams(name=data['team'], email=data['email'])
                            team.save()

                            # loop through members
                            for member in data['members']:
                                member["team"] = team.id
                                print(member)
                                requests.post(f'http://{request.get_host()}/api/members', json=member)

                            # create assoc team <-> bars
                            all_bars = Bars.objects.all()
                            for bar in all_bars:
                                # check if the assoc already exists
                                try:
                                    TeamsBars.objects.get(barId=bar, teamId=team)
                                except TeamsBars.DoesNotExist:
                                    team_bars_assoc = TeamsBars(teamId=team, barId=bar)                        
                                    team_bars_assoc.save()

                            # qr code generation
                            qr_name = f'qrcodes/qr_team{team.id}.png'
                            path = f'{BASE_DIR}/static/{qr_name}'
                            team.qr_code = f'http://{request.get_host()}/static/{qr_name}'

                            _generate_qrcode(path, 'http://127.0.0.1:8000/api/docs/')

                            team.save()
                            
                            response = {
                                "status": status.HTTP_200_OK,
                                "message": f"Added team {data['team']} successfully"
                            }
                            logger.info(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]}')
                            return Response(response, status=response["status"])
                        except Exception as e:
                            team.delete()

                            response = {
                                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                                "message": f"Could not add team {data['team']}"
                            }
                            logger.error(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]} ({e})')
                            return Response(response, status=response["status"])
                else:
                    response = {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "A team must have at least one member"
                    }
                    logger.error(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]}')
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
    
    if request.method == "GET":
        if id is not None:
            try:
                team = _get_team(Teams.objects.get(id=id))

                if request.auth and request.auth.key:
                    logger.info(request.auth.key, f'[{status.HTTP_200_OK}]@"{request.path}": Got team "{team["name"]}"')
                return Response(team, status=status.HTTP_200_OK)
            except Teams.DoesNotExist as e:
                response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": f"There is no team with the id {id}"
                }
                if request.auth and request.auth.key:
                    logger.error(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]} ({e})')
                return Response(response, status=response["status"]) 
        else:
            # check for other ways of team identification
            try:
                if request.GET.get("name"):
                    team_objects = [Teams.objects.get(name=request.GET.get("name"))]
                elif request.GET.get("email"):
                    team_objects = [Teams.objects.get(email=request.GET.get("email"))]
                elif request.GET.get("id"):
                    team_objects = [Teams.objects.get(id=request.GET.get("id"))]
                else:
                    # return all teams
                    team_objects = Teams.objects.all()

                teams = [_get_team(team_object) for team_object in team_objects]

                if request.auth and request.auth.key:
                    team_names = ", ".join([f'"{team["name"]}"' for team in teams])
                    logger.info(request.auth.key, f'[{status.HTTP_200_OK}]@"{request.path}": Got teams {team_names} successfully')
                return Response(teams[0] if len(teams) == 1 else teams, status=status.HTTP_200_OK)
            except Teams.DoesNotExist as e:
                response = {
                    "status": HTTP_400_BAD_REQUEST,
                    "message": f"There is no team with that identification"
                }
                if request.auth and request.auth.key:
                    logger.error(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]} ({e})')
                return Response(response, status=response["status"]) 

    if request.method == "DELETE":
        if id is not None:
            try:
                team= Teams.objects.get(id=id)

                # delete qrcode
                os.remove(f'{BASE_DIR}/static/qrcodes/qr_team{team.id}.png')

                team.delete()

                response = {
                    "status": status.HTTP_200_OK,
                    "message": f"Deleted team {team.name} successfully"
                }
                logger.warning(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]}')
                return Response(response, status=response["status"])
            except Teams.DoesNotExist as e:
                response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": f"There is no team with the id {id}"
                }
                logger.error(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]} ({e})')
                return Response(response, status=response["status"])
        else:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Missing team identifier"
            }
            logger.error(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]}')
            return Response(response, status=response["status"])

    if request.method == "PATCH":
        try:
            data = json.loads(request.body)
            if id is not None:
                try:
                    team = Teams.objects.get(id=id)
                    modifiable_fields = ["name", "email", "points", "drinks", "has_egg", "puked"]
                    for field in modifiable_fields:
                        if field in data:
                            # if field is name, check if it already exists
                            if field == "name":
                                try:
                                    Teams.objects.get(name=data[field])
                                    response = {
                                        "status": status.HTTP_400_BAD_REQUEST,
                                        "message": f"A team with the name {data[field]} already exists"
                                    }
                                    logger.error(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]}')
                                    return Response(response, status=response["status"])
                                except Teams.DoesNotExist:
                                    pass
                                
                            setattr(team, field, data[field])

                    team.save()
                    response = {
                        "status": status.HTTP_200_OK,
                        "message": f"Updated team {team.name} successfully"
                    }
                    logger.info(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]}')
                    return Response(response, status=response["status"])
                except Teams.DoesNotExist as e:
                    response = {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": f"There is no team with the id {id}"
                    }
                    logger.error(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]} ({e})')
                    return Response(response, status=response["status"])
            else:
                response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Missing team identifier"
                }
                logger.error(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]}')
                return Response(response, status=response["status"])
        except ValueError as e:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid JSON format"
            }
            logger.error(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]} ({e})')
            return Response(response, status=response["status"])

def _get_team(team_object):
    team = model_to_dict(team_object)

    # get members from this team
    team["members"] = [model_to_dict(member) for member in Members.objects.filter(team=team['id'])]

    # get bars from this team
    team_bars = [model_to_dict(row) for row in TeamsBars.objects.filter(teamId=team['id'])]
    team["bars"] = [
        {
            "id": bar["barId"],
            "bar": model_to_dict(Bars.objects.get(id=bar['barId'])),
            "points": bar['points'],
            'drinks': bar['drinks'],
            "has_egg": bar['has_egg'],
            "puked": bar['puked'],
            "visited": bar['visited'],
            "won_game": bar['won_game']
        }
    for bar in team_bars]

    return team


@api_view(["POST", "GET", "DELETE", "PATCH"])
@permission_classes((IsAuthenticatedOrReadOnly,))
@csrf_exempt
def members(request, id=None):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            try:
                try:
                    Members.objects.get(nmec=data["nmec"])

                    # if already exists, break
                    response = {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": f"A member with the nmec {data['nmec']} already exists"
                    }
                    logger.error(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]}')
                    return Response(response, status=response["status"])
                except Members.DoesNotExist:
                    try:
                        team = Teams.objects.get(id=float(data['team']))
                    except ValueError as e:
                        response = {
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": "Team id must be a number"
                        }
                        logger.error(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]} ({e})')
                        return Response(response, status=response["status"])

                    member = Members(name=data['name'], nmec=data['nmec'], course=data['course'], team=team)

                    try:
                        member.save()

                        # create assoc member <-> bars
                        all_bars = Bars.objects.all()
                        for bar in all_bars:
                            # check if the assoc already exists
                            try:
                                MembersBars.objects.get(barId=bar, memberId=member)
                            except MembersBars.DoesNotExist:
                                member_bars_assoc = MembersBars(barId=bar, memberId=member)                        
                                member_bars_assoc.save()

                        response = {
                            "status": status.HTTP_200_OK,
                            "message": f"Added member {data['name']} successfully to team {team.id}"
                        }
                        logger.info(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]}')
                        return Response(response, status=response["status"])
                    except Exception as e:
                        member.delete()

                        response = {
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": f"Error adding member {data['name']}"
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
        
    if request.method == "GET":
        if id is not None:
            try:
                member = _get_member(Members.objects.get(id=id))

                return Response(member, status=status.HTTP_200_OK) 
            except Teams.DoesNotExist as e:
                response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": f"There is no member with the id {id}"
                }
                if request.auth and request.auth.key:
                    logger.error(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]} ({e})')
                return Response(response, status=response["status"])
        else:
            # check for other ways of member identification
            try:
                if request.GET.get("name"):
                    member_objects = [Members.objects.get(name=request.GET.get("name"))]
                elif request.GET.get("nmec"):
                    member_objects = [Members.objects.get(email=request.GET.get("nmec"))]
                elif request.GET.get("id"):
                    member_objects = [Members.objects.get(id=request.GET.get("id"))]
                elif request.GET.get("course"):
                    member_objects = Members.objects.filter(id=request.GET.get("course"))
                else:
                    # return all members
                    member_objects = Members.objects.all()

                members = [_get_member(member) for member in member_objects]

                if request.auth and request.auth.key:
                    member_names = ", ".join([f'"{member["name"]}"' for member in members])
                    logger.info(request.auth.key, f'[{status.HTTP_200_OK}]@"{request.path}": Got teams {member_names} successfully')

                return Response(members[0] if len(members) == 1 else members, status=status.HTTP_200_OK)
            except Teams.DoesNotExist as e:
                response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": f"There is no member with that identification"
                }
                if request.auth and request.auth.key:
                    logger.error(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]} ({e})')
                return Response(response, status=response["status"])

    if request.method == "DELETE":
        if id is not None:
            try:
                member = Members.objects.get(id=id)
                member.delete()

                response = {
                    "status": status.HTTP_200_OK,
                    "message": f"Deleted member {member.name} successfully from team {member.team.name}"
                }
                logger.warning(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]}')
                return Response(response, status=response["status"])
            except Members.DoesNotExist as e:
                response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": f"There is no member with the id {id}"
                }
                logger.error(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]} ({e})')
                return Response(response, status=response["status"])
        else:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Missing member identifier"
            }
            logger.error(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]}')
            return Response(response, status=response["status"])
        
    if request.method == "PATCH":
        try:
            data = json.loads(request.body)
            if id is not None:
                try:
                    member = Members.objects.get(id=id)
                    modifiable_fields = ["name", "nmec", "course", "team", "points"]
                    for field in modifiable_fields:
                        if field in data:
                            # if field is nmec, check if it already exists
                            if field == "nmec":
                                try:
                                    Members.objects.get(nmec=data[field])
                                    response = {
                                        "status": status.HTTP_400_BAD_REQUEST,
                                        "message": f"Member with nmec {data[field]} already exists"
                                    }
                                    logger.error(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]}')
                                    return Response(response, status=response["status"])
                                except Members.DoesNotExist:
                                    pass
                                
                            setattr(member, field, data[field])

                    member.save()

                    response = {
                        "status": status.HTTP_200_OK,
                        "message": f"Updated member {member.name} successfully with nmec {member.nmec}"
                    }
                    logger.info(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]}')
                    return Response(response, status=response["status"])
                except Teams.DoesNotExist as e:
                    response = {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": f"There is no member with the id {id}"
                    }
                    logger.error(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]} ({e})')
                    return Response(response, status=response["status"])
            else:
                response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Missing member identifier"
                }
                logger.error(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]}')
                return Response(response, status=response["status"])
        except ValueError as e:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid JSON format"
            }
            logger.error(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]} ({e})')
            return Response(response, status=response["status"])

def _get_member(member_object):
    member = model_to_dict(member_object)

    # get team from this member
    member["team"] = model_to_dict(member_object.team)

    # get bars from this member
    member_bars = [model_to_dict(row) for row in MembersBars.objects.filter(memberId=member['id'])]
    member["bars"] = [
        {
            "id": bar["barId"],
            "bar": model_to_dict(Bars.objects.get(id=bar['barId'])),
            "points": bar['points'],
            'drinks': bar['drinks']
        }
        for bar in member_bars]

    return member


@api_view(["POST", "GET", "DELETE", "PATCH"])
@permission_classes((IsAuthenticatedOrReadOnly,))
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
                    if "game" in data:
                        game = Games.objects.get(id=data["game"])
                        bar = Bars(name=data['name'], address=data['address'], latitude=data['latitude'], longitude=data['longitude'], picture=data['picture'], game=game)
                    else:
                        bar = Bars(name=data['name'], address=data['address'], latitude=data['latitude'], longitude=data['longitude'], picture=data['picture'])

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

                        # fill MembersBars
                        all_members = Members.objects.all()
                        for member in all_members:
                            # check if the assoc already exists
                            try:
                                MembersBars.objects.get(barId=bar, memberId=member)
                            except MembersBars.DoesNotExist:
                                member_bars_assoc = MembersBars(barId=bar, memberId=member)
                                member_bars_assoc.save()

                        return Response({
                            "status": 200,
                            "message": f"Added bar {data['name']} successfully"
                        }, status=status.HTTP_200_OK)
                    except Exception as e:
                        # bar.delete()

                        return Response({
                            "status": 500,
                            "message": f"Could not add bar {data['name']}",
                            "error": str(e)
                        },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
                bar_object = Bars.objects.get(id=id)
                bar = model_to_dict(bar_object)

                if bar_object.game is not None:
                    bar["game"] = model_to_dict(bar_object.game)

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
                elif request.GET.get("id"):
                    bar_objects = [Bars.objects.get(id=request.GET.get("id"))]
                else:
                    # return all teams
                    bar_objects = Bars.objects.all()

                bars = []
                for bar_object in bar_objects:
                    bar = model_to_dict(bar_object)
                    if bar_object.game is not None:
                        bar["game"] = model_to_dict(bar_object.game)
                    
                    bars.append(bar)

                return Response(bars[0] if len(bars) == 1 else bars, status=status.HTTP_200_OK)
            except Bars.DoesNotExist:
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

    if request.method == "PATCH":
        try:
            data = json.loads(request.body)
            if id is not None:
                try:
                    bar = Bars.objects.get(id=id)
                    modifiable_fields = ["name", "address", "latitude", "longitude", "picture", "points", "drinks", "puked", "visited", "game"]
                    for field in modifiable_fields:
                        if field in data:
                            # if field is name, check if it already exists
                            if field == "name":
                                try:
                                    Bars.objects.get(name=data[field])
                                    return Response({
                                        "status": 400,
                                        "message": f"A bar with the name {data[field]} already exists"
                                    }, status=status.HTTP_400_BAD_REQUEST)
                                except Members.DoesNotExist:
                                    pass

                            # if field is game, check if it exists
                            if field == "game":
                                try:
                                    game = Games.objects.get(id=data[field])
                                    setattr(bar, field, game)
                                    continue
                                except Games.DoesNotExist:
                                    return Response({
                                        "status": 400,
                                        "message": f"There is no game with the id {data[field]}"
                                    }, status=status.HTTP_400_BAD_REQUEST)
                                
                            setattr(bar, field, data[field])

                    bar.save()
                    return Response({
                        "status": 200,
                        "message": f"Updated bar {bar.name}"
                    }, status=status.HTTP_200_OK) 
                except Teams.DoesNotExist:
                    return Response({
                        "status": 400,
                        "message": f"There is no bar with the id {id}"
                    }, status=status.HTTP_400_BAD_REQUEST) 
            else:
                return Response({
                    "status": 400,
                    "message": "Missing bar identifier"
                }, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({
                "status": 400,
                "message": "Invalid JSON format",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST", "GET"])
@csrf_exempt
def points(request, id=None, method=None):
    if id is not None:
        if request.method == "POST":
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

        if request.method == "GET":
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
    
    else:
        return Response({
            "status": 400,
            "message": "Missing team ID"
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST", "GET", "DELETE"])
@permission_classes((IsAuthenticatedOrReadOnly,))
@csrf_exempt
def qrcodes(request, id=None):
    if id is not None:
        try:
            team = Teams.objects.get(id=id)

            # generate qrcode
            if request.method == "POST":
                qr_name = f'qrcodes/qr_team{id}.png'
                path = f'{BASE_DIR}/static/{qr_name}'
                team.qr_code = f'http://{request.get_host()}/static/{qr_name}'

                _generate_qrcode(path, 'http://127.0.0.1:8000/api/docs/')

                team.save()

                return Response({
                    "status": 200,
                    "message": f"Created qrcode at {qr_name} for team {team.id}"
                },status=status.HTTP_200_OK)

            # get qrcode path
            if request.method == "GET":
                return redirect(f'/static/qrcodes/qr_team{team.id}.png')

            if request.method == "DELETE":
                os.remove(f'{BASE_DIR}/static/qrcodes/qr_team{team.id}.png')
                
                return Response({
                    "status": 200,
                    "message": f"Deleted qrcode for team {team.id}"
                },status=status.HTTP_200_OK)

        except Teams.DoesNotExist:
            return Response({
                "status": 400,
                "message": f"A team with the id {id} doesn't exist"
            },status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({
            "status": 400,
            "message": "Missing team ID"
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST", "GET", "DELETE", "PATCH"])
@permission_classes((IsAuthenticatedOrReadOnly,))
@csrf_exempt
def games(request, id=None):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            try:
                try:
                    Games.objects.get(name=data["name"])

                    # if already exists, break
                    return Response({
                        "status": 400,
                        "message": f"A game with the name {data['name']} already exists"
                    }, status=status.HTTP_400_BAD_REQUEST)
                except Games.DoesNotExist:
                    game = Games(name=data['name'], description=data['description'], points=data['points'])

                    try:
                        game.save()

                        return Response({
                            "status": 200,
                            "message": f"Added game {data['name']} successfully"
                        }, status=status.HTTP_200_OK)
                    except Exception:
                        game.delete()

                        return Response({
                            "status": 500,
                            "message": f"Could not add game {data['name']}"
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
                game_object = Games.objects.get(id=id)
                game = model_to_dict(game_object)

                return Response(game, status=status.HTTP_200_OK) 
            except Games.DoesNotExist:
                return Response({
                    "status": 400,
                    "message": f"There is no game with the id {id}"
                }, status=status.HTTP_400_BAD_REQUEST) 
        else:
            # check for other ways of game identification
            try:
                if request.GET.get("name"):
                    game_objects= [Games.objects.get(name=request.GET.get("name"))]
                elif request.GET.get("id"):
                    game_objects = [Games.objects.get(id=request.GET.get("id"))]
                elif request.GET.get("points"):
                    game_objects = Games.objects.filter(points=request.GET.get("points"))
                else:
                    # return all teams
                    game_objects = Games.objects.all()

                games = []
                for game_object in game_objects:
                    game = model_to_dict(game_object)
                    games.append(game)

                return Response(games[0] if len(games) == 1 else games, status=status.HTTP_200_OK)
            except Games.DoesNotExist:
                return Response({
                    "status": 400,
                    "message": f"There is no bar with that identification"
                }, status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == "DELETE":
        if id is not None:
            try:
                game = Games.objects.get(id=id)
                game.delete()

                return Response({
                    "status": 200,
                    "message": f"Deleted game {game.name}"
                }, status=status.HTTP_200_OK) 
            except Games.DoesNotExist:
                return Response({
                    "status": 400,
                    "message": f"There is no game with the id {id}"
                }, status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response({
                "status": 400,
                "message": "Missing game identifier"
            }, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "PATCH":
        try:
            data = json.loads(request.body)
            if id is not None:
                try:
                    game = Games.objects.get(id=id)
                    modifiable_fields = ["name", "location", "points"]
                    for field in modifiable_fields:
                        if field in data:
                            # if field is name, check if it already exists
                            if field == "name":
                                try:
                                    Games.objects.get(name=data[field])
                                    return Response({
                                        "status": 400,
                                        "message": f"A game with the name {data[field]} already exists"
                                    }, status=status.HTTP_400_BAD_REQUEST)
                                except Games.DoesNotExist:
                                    pass
                                
                            setattr(game, field, data[field])

                    game.save()
                    return Response({
                        "status": 200,
                        "message": f"Updated game {game.name}"
                    }, status=status.HTTP_200_OK) 
                except Teams.DoesNotExist:
                    return Response({
                        "status": 400,
                        "message": f"There is no game with the id {id}"
                    }, status=status.HTTP_400_BAD_REQUEST) 
            else:
                return Response({
                    "status": 400,
                    "message": "Missing game identifier"
                }, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({
                "status": 400,
                "message": "Invalid JSON format",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST", "GET", "DELETE", "PATCH"])
@permission_classes((IsAuthenticatedOrReadOnly,))
@csrf_exempt
def prizes(request, id=None):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            try:
                try:
                    Prizes.objects.get(name=data["name"])

                    # if already exists, break
                    return Response({
                        "status": 400,
                        "message": f"A prize with the name {data['name']} already exists"
                    }, status=status.HTTP_400_BAD_REQUEST)
                except Prizes.DoesNotExist:
                    prize = Prizes(name=data['name'], place=data['place'], ammount=data['ammount'])

                    try:
                        prize.save()

                        return Response({
                            "status": 200,
                            "message": f"Added prize {data['name']} successfully"
                        }, status=status.HTTP_200_OK)
                    except Exception:
                        prize.delete()

                        return Response({
                            "status": 500,
                            "message": f"Could not add prize {data['name']}"
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
                prize_object = Prizes.objects.get(id=id)
                prize = model_to_dict(prize_object)

                # get winner if exists
                if prize_object.winner is not None:
                    prize["winner"] = model_to_dict(prize_object.winner)

                return Response(prize, status=status.HTTP_200_OK) 
            except Prizes.DoesNotExist:
                return Response({
                    "status": 400,
                    "message": f"There is no prize with the id {id}"
                }, status=status.HTTP_400_BAD_REQUEST) 
        else:
            # check for other ways of game identification
            try:
                if request.GET.get("name"):
                    prize_objects = [Prizes.objects.get(name=request.GET.get("name"))]
                elif request.GET.get("id"):
                    prize_objects = [Prizes.objects.get(id=request.GET.get("id"))]
                elif request.GET.get("place"):
                    prize_objects = [Prizes.objects.get(place=request.GET.get("place"))]
                elif request.GET.get("ammount"):
                    prize_objects = Prizes.objects.filter(ammount=request.GET.get("ammount"))
                else:
                    # return all teams
                    prize_objects = Prizes.objects.all()

                prizes = []
                for prize_object in prize_objects:
                    prize = model_to_dict(prize_object)
                    
                    # get winner if exists
                    if prize_object.winner is not None:
                        prize["winner"] = model_to_dict(prize_object.winner)
                    
                    prizes.append(prize)

                return Response(prizes[0] if len(prizes) == 1 else prizes, status=status.HTTP_200_OK)
            except Prizes.DoesNotExist:
                return Response({
                    "status": 400,
                    "message": f"There is no bar with that identification"
                }, status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == "DELETE":
        if id is not None:
            try:
                prize = Prizes.objects.get(id=id)
                prize.delete()

                return Response({
                    "status": 200,
                    "message": f"Deleted prize {prize.name}"
                }, status=status.HTTP_200_OK) 
            except Prizes.DoesNotExist:
                return Response({
                    "status": 400,
                    "message": f"There is no prize with the id {id}"
                }, status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response({
                "status": 400,
                "message": "Missing prize identifier"
            }, status=status.HTTP_400_BAD_REQUEST) 

    if request.method == "PATCH":
        try:
            data = json.loads(request.body)
            if id is not None:
                try:
                    prize = Prizes.objects.get(id=id)
                    modifiable_fields = ["name", "place", "ammount", "winner"]
                    for field in modifiable_fields:
                        if field in data:
                            # if field is place, check if it is already taken
                            if field == "place":
                                try:
                                    Prizes.objects.get(place=data[field])
                                    return Response({
                                        "status": 400,
                                        "message": f"A prize for the place {data[field]} already exists"
                                    }, status=status.HTTP_400_BAD_REQUEST)
                                except Prizes.DoesNotExist:
                                    pass

                            # if field is winner, make sure the team exists
                            if field == "winner":
                                try:
                                    team = Teams.objects.get(id=data[field])
                                    setattr(prize, field, team)
                                    continue
                                except Teams.DoesNotExist:
                                    return Response({
                                        "status": 400,
                                        "message": f"There is no team with the id {data[field]}"
                                    }, status=status.HTTP_400_BAD_REQUEST)
                                
                            setattr(prize, field, data[field])

                    prize.save()
                    return Response({
                        "status": 200,
                        "message": f"Updated prize {prize.name}"
                    }, status=status.HTTP_200_OK) 
                except Teams.DoesNotExist:
                    return Response({
                        "status": 400,
                        "message": f"There is no prize with the id {id}"
                    }, status=status.HTTP_400_BAD_REQUEST) 
            else:
                return Response({
                    "status": 400,
                    "message": "Missing prize identifier"
                }, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({
                "status": 400,
                "message": "Invalid JSON format",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

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
            return points + value
        elif method == "remove":
            return points - value
        elif method == "set":
            return value

        return points


def _generate_qrcode(path, data):
    l = [RadialGradiantColorMask(), SquareGradiantColorMask(), HorizontalGradiantColorMask(), VerticalGradiantColorMask()]
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        border=2
    )
    qr.add_data(data)

    img = qr.make_image(image_factory=StyledPilImage, color_mask=l[random.randint(0,3)])
    img.save(path)