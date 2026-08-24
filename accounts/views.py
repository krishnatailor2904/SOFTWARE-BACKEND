from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile


class RegisterView(APIView):
    """
    POST /api/auth/register/
    body: { username, password, shop_name, phone (optional) }
    Naya shop-owner account banata hai aur seedha login (token) bhi de deta hai.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = (request.data.get('username') or '').strip()
        password = request.data.get('password') or ''
        shop_name = (request.data.get('shop_name') or '').strip()
        phone = (request.data.get('phone') or '').strip()

        if not username or not password or not shop_name:
            return Response(
                {'error': 'Username, password aur shop/brand ka naam — teeno zaroori hain.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(password) < 4:
            return Response(
                {'error': 'Password kam se kam 4 characters ka hona chahiye.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if User.objects.filter(username__iexact=username).exists():
            return Response(
                {'error': 'Ye username pehle se registered hai. Dusra username try karo ya login karo.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create_user(username=username, password=password)
        profile = Profile.objects.create(user=user, shop_name=shop_name, phone=phone)
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {'token': token.key, 'username': user.username, 'shop_name': profile.shop_name},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """
    POST /api/auth/login/
    body: { username, password }
    Pehle se registered user ko login karwata hai — uska purana data
    (bills, measurements) automatically usi ke account me milega.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = (request.data.get('username') or '').strip()
        password = request.data.get('password') or ''

        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {'error': 'Username ya password galat hai.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token, _ = Token.objects.get_or_create(user=user)
        profile, _ = Profile.objects.get_or_create(user=user, defaults={'shop_name': user.username})

        return Response({'token': token.key, 'username': user.username, 'shop_name': profile.shop_name})


class MeView(APIView):
    """
    GET /api/auth/me/
    Login hua hua user apna shop_name/username dobara le sakta hai
    (page reload hone par header me naam dikhane ke liye use hota hai).
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, _ = Profile.objects.get_or_create(
            user=request.user, defaults={'shop_name': request.user.username}
        )
        return Response({'username': request.user.username, 'shop_name': profile.shop_name})
