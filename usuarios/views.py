from rest_framework import generics, permissions, views, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from .models import CustomUser
from . serializers import UserSerializer, RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def put(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def get_object(self):
        user = self.request.user
        return user
    

class VerifyTokenView(views.APIView):
    def post(self, request):
        token = request.data.get("access_token")
        if not token:
            return Response({"error": "Token não fornecido"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            access_token = AccessToken(token)
            return Response({
                "valid": True,
                "payload": access_token.payload,
            }, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({"error": f"Token inválido: {str(e)}"}, status=status.HTTP_401_UNAUTHORIZED)