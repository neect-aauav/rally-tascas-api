import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import RegistrationSerializer
from management import logger

from api.models import Bars
from django.forms.models import model_to_dict

@api_view(["POST"])
@permission_classes((IsAuthenticated,))
@csrf_exempt
def register(request):
    if request.method == "POST":
        if request.user.is_superuser:
            serializer = RegistrationSerializer(data=request.data)
            if serializer.is_valid():
                account = serializer.save()
                token = Token.objects.get(user=account).key

                response = {
                    "status": status.HTTP_201_CREATED,
                    "message": f"Successfully created admin user {account.username}",
                    "token": token
                }
                logger.info(request.auth.key, f'[{response["status"]}]@"{request.method} {request.path}": {response["message"]}')
                return Response(response, status=response["status"])
            else:
                response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": f"Failed to create admin user {request.data['username']}"
                }
                logger.error(request.auth.key, f'[{response["status"]}]@"{request.method} {request.path}": {response["message"]}')
                return Response(response, status=response["status"])
        else:
            response = {
                "status": status.HTTP_401_UNAUTHORIZED,
                "message": "You are not authorized to create admin users"
            }
            logger.warning(request.auth.key, f'[{response["status"]}]@"{request.method} {request.path}": {response["message"]}')
            return Response(response, status=response["status"])


@api_view(["POST"])
@permission_classes((AllowAny,))
@csrf_exempt
def check_token(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        
            token = Token.objects.get(key=data["token"])
            user = token.user

            response = {
                "status": status.HTTP_200_OK,
                "message": f"Token {data['token']} is valid",
                "valid": True,
            }
            if request.auth and request.auth.key:
                logger.info(request.auth.key, f'[{response["status"]}]@"{request.method} {request.path}": {response["message"]}')
            return Response(response, status=response["status"])
        except Token.DoesNotExist as e:
            response = {
                "status": status.HTTP_401_UNAUTHORIZED,
                "message": f"Token {data['token']} is invalid",
                "valid": False
            }
            if request.auth and request.auth.key:
                logger.error(request.auth.key, f'[{response["status"]}]@"{request.method} {request.path}": {response["message"]} ({e})')
            return Response(response, status=response["status"])
        except Exception as e:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": f"Failed to check token",
            }
            if request.auth and request.auth.key:
                logger.error(request.auth.key, f'[{response["status"]}]@"{request.method} {request.path}": {response["message"]} ({e})')
            return Response(response, status=response["status"])


@api_view(["GET", "PATCH"])
@permission_classes((IsAuthenticated,))
@csrf_exempt
def admin(request, token=None):
    if request.method == "GET":
        # if not super user, only show its own information
        print(request.auth.key, token, request.user.is_superuser)
        if request.auth.key == token or request.user.is_superuser:
            try:
                token = Token.objects.get(key=token)
                user = token.user

                response = {
                    "status": status.HTTP_200_OK,
                    "message": f"Successfully fetched admin user {user.username}",
                    "user": {
                        "username": user.username,
                        "is_superuser": user.is_superuser,
                        "name": user.name,
                        "nmec": user.nmec,
                        "last_login": user.last_login,
                        "date_joined": user.date_joined,
                        "is_admin": user.is_admin,
                        "is_staff": user.is_staff
                    }
                }

                if user.bar:
                    try:
                        bar = Bars.objects.get(id=user.bar.id)
                        response["user"]["bar"] = model_to_dict(bar)
                    except Bars.DoesNotExist:
                        response["user"]["bar"] = None
                else:
                    response["user"]["bar"] = None

                logger.info(request.auth.key, f'[{response["status"]}]@"{request.method} {request.path}": {response["message"]}')
                return Response(response["user"], status=response["status"])
            except Token.DoesNotExist as e:
                response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": f"Admin user with token {token} does not exist"
                }
                logger.error(request.auth.key, f'[{response["status"]}]@"{request.method} {request.path}": {response["message"]} ({e})')
                return Response(response, status=response["status"])
            except Exception as e:
                response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": f"Failed to fetch admin user with token {token}"
                }
                logger.error(request.auth.key, f'[{response["status"]}]@"{request.method} {request.path}": {response["message"]} ({e})')
                return Response(response, status=response["status"])
        else:
            response = {
                "status": status.HTTP_401_UNAUTHORIZED,
                "message": "You are not authorized to fetch other users"
            }
            logger.warning(request.auth.key, f'[{response["status"]}]@"{request.method} {request.path}": {response["message"]}')
            return Response(response, status=response["status"])
    elif request.method == "PATCH":
        if request.auth.key == token or request.user.is_superuser:
            try:
                token = Token.objects.get(key=token)
                user = token.user

                data = json.loads(request.body)
                modifiable_fields = ["username", "password", "name", "nmec", "bar"]
                for field in modifiable_fields:
                    if field in data:
                        if field == "password":
                            user.set_password(data[field])
                        if field == "bar":
                            try:
                                bar = Bars.objects.get(id=data[field])
                                user.bar = bar
                            except Bars.DoesNotExist:
                                continue
                        else:
                            setattr(user, field, data[field])
                
                user.save()

                response = {
                    "status": status.HTTP_200_OK,
                    "message": f"Successfully updated admin user {user.username}",
                }
                logger.info(request.auth.key, f'[{response["status"]}]@"{request.method} {request.path}": {response["message"]}')
                return Response(response, status=response["status"])
            except Token.DoesNotExist as e:
                response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": f"Admin user with token {token} does not exist"
                }
                logger.error(request.auth.key, f'[{response["status"]}]@"{request.method} {request.path}": {response["message"]} ({e})')
                return Response(response, status=response["status"])
            except Exception as e:
                response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": f"Failed to update admin user with token {token}"
                }
                logger.error(request.auth.key, f'[{response["status"]}]@"{request.method} {request.path}": {response["message"]} ({e})')
                return Response(response, status=response["status"])
        else:
            response = {
                "status": status.HTTP_401_UNAUTHORIZED,
                "message": "You are not authorized to update other users"
            }
            logger.warning(request.auth.key, f'[{response["status"]}]@"{request.method} {request.path}": {response["message"]}')
            return Response(response, status=response["status"])