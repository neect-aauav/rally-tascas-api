from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from .serializers import RegistrationSerializer
from management import logger

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
                logger.info(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]}')
                return Response(response, status=response["status"])
            else:
                response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": f"Failed to create admin user {request.data['username']}"
                }
                logger.error(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]}')
                return Response(response, status=response["status"])
        else:
            response = {
                "status": status.HTTP_401_UNAUTHORIZED,
                "message": "You are not authorized to create admin users"
            }
            logger.warning(request.auth.key, f'[{response["status"]}]@"{request.path}": {response["message"]}')
            return Response(response, status=response["status"])