from django.contrib.auth.models import AbstractUser
from django.db import models

# admin: admin (superuser)


class User(AbstractUser):
    """
    This class inherits from Django's AbstractUser class and facilitates user registeration in the application.

    Also creates watchlist for each user.
    """
    watchlist = models.ManyToManyField('Listing', blank=True)


class Listing(models.Model):
    """
    This class represents a Listing in the application.

    Each listing has a number of fields, which contain the metadata for that listing.
    Each listing is associated with a User who created that listing, and a User who has won that auction.
    """
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    start_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(blank=True)
    CATEGORIES_CHOICES = (
        ('', '-----------------'),
        ('GM', 'General Merchandise'),
        ('EL', 'Electronics'),
        ('FA', 'Fashion'),
        ('HG', 'Home & Garden'),
        ('HB', 'Health & Beauty'),
        ('TH', 'Toys & Hobbies'),
        ('SO', 'Sports & Outdoors'),
        ('ME', 'Media & Entertainment'),
        ('AU', 'Automotive'),
        ('MS', 'Miscellaneous')
    )
    category = models.CharField(
        max_length=64, choices=CATEGORIES_CHOICES, default='', blank=True)
    active = models.BooleanField(default=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings")
    winner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="winner", blank=True, null=True
    )

    def __str__(self):
        return f"{self.title} is {'active' if self.active else 'inactive'} in {self.category} by {self.author}"


class Bid(models.Model):
    """
    This class represents Bids in the application.

    Each Bid entry is associated with a User and a Listing.
    Bid.bid is a decimal field that can have decimals to two decimal places.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bids"
    )
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="bids"
    )
    bid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.bid}"


# Moved to User Class for efficiency
# class Watchlist(models.Model):
#     """
#     This class represents a Watchlist in the application.

#     Each Watchlist is associated with a User and a Listing.
#     The 'watchlist' field indicates whether the User has added the Listing to their Watchlist.
#     If 'watchlist' is True, the Listing is on the User's Watchlist; if NULL or False, it is not.
#     """
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name="watchlist"
#     )
#     listing = models.ForeignKey(
#         Listing, on_delete=models.CASCADE, related_name="watchlist"
#     )
#     watchlist = models.BooleanField(default=None, null=True)


class Comment(models.Model):
    """
    This class represents a Comment in the application.

    Each Comment is associated with a User and a Listing.
    'Comment.comment' is text field that contains the actual comment a user made on a listing.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comments", null=False
    )
    comment = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.comment}"
