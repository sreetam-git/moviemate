from django.forms import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from user_app.api.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from user_app import models

@api_view(['POST',])
def logout_view(request):
    # Perform logout logic here
    # Delete the user's token
    if request.method == 'POST':
        Token.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_200_OK)

@api_view(['POST',])
@authentication_classes([])  # Disables authentication for this view
@permission_classes([]) 
def registration_view(request):
    if request.method == 'POST':
        # Perform form validation and registration logic here
        data = {}
        serializer = RegistrationSerializer(data = request.data)
        if serializer.is_valid():
            user_response = serializer.save()
            data['response'] = 'Registration successful'
            data['username'] = user_response.username
            data['email'] = user_response.email
            
            # token = Token.objects.get(user = user_response).key
            # data['token'] = token
            refresh = RefreshToken.for_user(user_response)
            data['token'] = {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
            
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Render registration form template
        raise ValidationError("Unable to serialize registration")