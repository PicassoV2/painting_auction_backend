from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_painter = models.BooleanField(default=False)  # Whether the user is a painter
    is_painter_requested = models.BooleanField(default=False)  # Painter request status
    is_painter_approved = models.BooleanField(default=False)  # Add this field


    def __str__(self):
        return self.user.username

# API/models.py
class Painting(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="paintings")
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='paintings/')
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved_for_bidding = models.BooleanField(default=False)  # New field to approve for bidding

    def __str__(self):
        return self.title

class Auction(models.Model):
    painting = models.OneToOneField(Painting, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"Auction for {self.painting.title}"


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(Profile, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder.user.username}'s bid of {self.bid_amount} on {self.auction.painting.title}"


class Payment(models.Model):
    bid = models.OneToOneField(Bid, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])

    def __str__(self):
        return f"Payment for {self.bid.auction.painting.title} by {self.bid.bidder.user.username}"


class Comment(models.Model):
    painting = models.ForeignKey(Painting, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.commenter.user.username}'s comment on {self.painting.title}"


class Rating(models.Model):
    painter = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="ratings")
    rater = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="given_ratings")
    rating_value = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating {self.rating_value} by {self.rater.user.username} for {self.painter.user.username}"
