from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, ProfileSerializer, PaintingSerializer
from .models import Profile, Painting
from rest_framework.permissions import IsAuthenticated
from cloudinary_storage.storage import MediaCloudinaryStorage


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.filter(username=username).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({"detail": "Invalid credentials"}, status=400)

class HomeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({"message": "Welcome to the Home Page!"})

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is logged in

    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)  # Get the profile for the current user
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class ApplyToBecomePainterView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is logged in

    def post(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        if not profile.is_painter_requested:
            # User requests to become a painter
            profile.is_painter_requested = True
            profile.save()
            return Response({"message": "Painter request submitted."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Request already submitted."}, status=status.HTTP_400_BAD_REQUEST)

class PaintingListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = request.user.profile
        if not user_profile.is_painter_approved:
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
        
        paintings = Painting.objects.filter(profile=user_profile)
        serializer = PaintingSerializer(paintings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user_profile = request.user.profile
        if not user_profile.is_painter_approved:
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = PaintingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(profile=user_profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # API/views.py
class PainterDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = request.user.profile
        if not user_profile.is_painter_approved:
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        # Fetch only approved paintings
        approved_paintings = user_profile.paintings.filter(is_approved_for_bidding=True)

        return Response({
            "profile": ProfileSerializer(user_profile).data,
            "approved_paintings": PaintingSerializer(approved_paintings, many=True).data
        }, status=status.HTTP_200_OK)
    
class PaintingListView(APIView):
    def get(self, request):
        paintings = Painting.objects.all()[:10]
        serializer = PaintingSerializer(paintings, many=True)
        return Response(serializer.data)

class UploadImageView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        image = request.FILES['image']
        storage = MediaCloudinaryStorage()
        image_url = storage.url(storage.save(image.name, image))
        painting = Painting(
            title=request.data['title'],
            description=request.data['description'],
            image=image_url,
            category=request.data['category'],
            profile=request.user.profile
        )
        painting.save()
        serializer = PaintingSerializer(painting)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
