from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status


class CustomTokenObtainPairView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['username', 'password']
        ),
        responses={
            200: openapi.Response(
                description="Token obtained",
                examples={
                    "application/json": {"token": "your_token_here"}
                }
            ),
            400: openapi.Response(
                description="Invalid credentials",
                examples={
                    "application/json": {"error": "Invalid credentials"}
                }
            ),
        }
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({
                "token": user.auth_token.key
            })
        else:
            return Response({"error": "Invalid credentials"}, status=400)
        
class CreateUser(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                'patronymic': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'birth_date': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['first_name', 'last_name', 'patronymic', 'email', 'password', 'birth_date']
        ),
        responses={
            200: openapi.Response(
                description="Token obtained",
                examples={
                    "application/json": {"name": "last_name"}
                }
            ),
            403: openapi.Response(
                description="Invalid credentials",
                examples={
                    "application/json": {"message": "Login failed"}
                }
            ),
        }
    )
    def post(self, request):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        patronymic = request.data.get('patronymic')
        email = request.data.get('email')
        password = request.data.get('password')
        birth_date = request.data.get('birth_date')

        # Проверка существования пользователя по email
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Создание пользователя
        user = User.objects.create(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save()

        # Можно также создать модель с дополнительными полями, связанной с пользователем
        # Например, CustomUserProfile для хранения patronymic и birth_date
        # CustomUserProfile.objects.create(
        #     user=user,
        #     patronymic=patronymic,
        #     birth_date=birth_date
        # )
        #user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({
                "message": "Пользователь создан"
            })
        else:
            return Response({"error": "Invalid credentials"}, status=403)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
            "full_name": f"{user.first_name} {user.last_name}",
        })

class UserItemsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response([{"item_id": "Foo", "owner": user.username}])
    
    