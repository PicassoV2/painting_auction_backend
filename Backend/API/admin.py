# API/admin.py
from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_painter', 'is_painter_requested', 'is_painter_approved')
    actions = ['approve_painter_requests']

    def approve_painter_requests(self, request, queryset):
        """Custom admin action to approve selected painter requests."""
        count = queryset.update(is_painter_approved=True, is_painter=True, is_painter_requested=False)
        self.message_user(request, f"{count} profile(s) successfully approved as painter.")

    approve_painter_requests.short_description = "Approve selected painter requests"
