from rest_framework import generics, permissions, views, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from .models import CustomUser
from .serializers import UserSerializer, RegisterSerializer
from django.db.models import Q
from rest_framework import status
import datetime
from django.utils.dateparse import parse_date

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff and request.user.cargo == 'admin'

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = CustomUser.objects.all()
        search = self.request.query_params.get('search', '')
        status = self.request.query_params.get('status', 'all')
        data_inicio = self.request.query_params.get('data_inicio', '')
        data_fim = self.request.query_params.get('data_fim', '')

        # Search filter
        if search:
            queryset = queryset.filter(
                Q(nome__icontains=search) |
                Q(email__icontains=search) |
                Q(cpf__icontains=search)
            )

        # Status filter
        if status != 'all':
            is_active = status == 'active'
            queryset = queryset.filter(is_active=is_active)

        # Date range filter
        if data_inicio:
            start_date = parse_date(data_inicio)
            if start_date:
                queryset = queryset.filter(data_registro__date__gte=start_date)
        if data_fim:
            end_date = parse_date(data_fim)
            if end_date:
                queryset = queryset.filter(data_registro__date__lte=end_date)

        return queryset


class UserToggleStatusView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    

class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

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