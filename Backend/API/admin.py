# API/admin.py
from django.contrib import admin
from .models import Profile, Painting, Auction, Bid, Payment, Comment, Rating 

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_painter', 'is_painter_requested', 'is_painter_approved')
    actions = ['approve_painter_requests']

    def approve_painter_requests(self, request, queryset):
        """Custom admin action to approve selected painter requests."""
        count = queryset.update(is_painter_approved=True, is_painter=True, is_painter_requested=False)
        self.message_user(request, f"{count} profile(s) successfully approved as painter.")

    approve_painter_requests.short_description = "Approve selected painter requests"

@admin.action(description='Approve selected paintings for bidding')
def approve_paintings_for_bidding(modeladmin, request, queryset):
    queryset.update(is_approved_for_bidding=True)

class PaintingAdmin(admin.ModelAdmin):
    list_display = ['title', 'profile', 'created_at', 'is_approved_for_bidding']
    actions = [approve_paintings_for_bidding]  # Add the custom action

admin.site.register(Painting, PaintingAdmin)

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ['painting', 'start_time', 'end_time', 'starting_bid', 'is_active']

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ['auction', 'bidder', 'bid_amount', 'bid_time']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['bid', 'payment_date', 'payment_status']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['painting', 'commenter', 'created_at']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['painter', 'rater', 'rating_value', 'created_at']