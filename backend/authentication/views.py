#views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime
from .models import User

class Register(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Explicitly create a Response object with the serialized data
        response_data = {
            "message": "User registered successfully",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class Login(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data["password"]

        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed(f'user not found')
        if not  user.check_password(password):
            raise AuthenticationFailed('Incorrect password')
        
        payload = {
            'id' : user.id,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat' : datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        # response = Response(
        #     {
        #         'message' : 'User logged in successfully',
        #         'token' : token    
        #     },
        #     status=status.HTTP_200_OK
        # )

        response = Response()
        response.set_cookie('token', token, httponly=True)

        response.data = {
                'message' : 'User logged in successfully',
                'token' : token    
            }
        return response

class UserView(APIView):
    def get(self, request, *args, **kwargs):
        token = request.COOKIES['token']
        if not token:
            raise AuthenticationFailed('unauthenticated')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')
        
        user = User.objects.get(id=payload['id'])
        serializer = UserSerializer(user)

        return Response(serializer.data)


class Logout(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            # Update the is_logged_in status to False when the user logs out
            request.user.is_logged_in = False
            request.user.save()
        response = Response()
        response.delete_cookie('token')
        response.data = {
            'message' : 'User logged out successfully'
        }
        
        return response