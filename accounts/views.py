
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from .serializers import LoginSerializer, UserProfileSerializer


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        # Validação dos dados enviados
        if serializer.is_valid():

            user = authenticate(
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"]
            )

            # Verifica se encontrou um usuário válido
            if user is not None:

                # Busca ou cria o token de autenticação
                token, created = Token.objects.get_or_create(user=user)

                return Response(
                    {"token": token.key},
                    status=status.HTTP_200_OK
                )

            # Credenciais inválidas
            return Response(
                {"detail": "Usuário ou senha inválidos"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Dados inválidos
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()

        return Response(
            {"detail": "Logout realizado com sucesso."},
            status=status.HTTP_200_OK
        )


class UserProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)

        return Response(serializer.data)
