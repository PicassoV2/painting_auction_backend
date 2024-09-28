from django.urls import path
from .views import RegisterView, LoginView, HomeView, ProfileView, ApplyToBecomePainterView, PaintingListCreateView, PainterDashboardView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/become_painter/', ApplyToBecomePainterView.as_view(), name='apply_become_painter'),
    path('paintings/', PaintingListCreateView.as_view(), name='paintings'),
    path('dashboard/', PainterDashboardView.as_view(), name='dashboard'),
]