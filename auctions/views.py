from django import forms
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import User, Listing, Bid, Comment


class BidForm(forms.Form):
    """
    A Django form for submitting bids to an existing listing.
    """
    new_bid = forms.FloatField(
        label="", widget=forms.TextInput(attrs={"placeholder": "Bid", "class": "form-control"}))

    def __init__(self, *args, **kwargs):
        self.min_value = kwargs.pop('min_value', 0.0)
        super(BidForm, self).__init__(*args, **kwargs)

        def validate_greater_than_min(value):
            if float(value) <= float(self.min_value):
                raise ValidationError(
                    'Your bid must be higher than the current bid.')
        self.fields['new_bid'].validators.append(validate_greater_than_min)


class NewListingForm(forms.ModelForm):
    """
    A Django form for creating a new listing, inheriting from 'models.Listing'.
    """
    class Meta:
        model = Listing
        exclude = ['author', 'active', 'winner']

    def __init__(self, *args, **kwargs):
        super(NewListingForm, self).__init__(*args, **kwargs)
        self.fields['start_bid'].label = "Starting Price"
        self.fields['image'].label = "Image URL"
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if not field.required:
                continue
            self.fields[field_name].label = f'*{field.label}'


class NewCommentForm(forms.ModelForm):
    class Comment:
        model = Comment


# Application View Functions
def index(request):
    """
    Renders the homepage with all of the active listings in the database.

    Parameters:
        request (HttpRequest): The request instance.

    Returns:
        HttpResponse: The response instance, rendering the index page with all active listings.
    """
    context = {"listings": Listing.objects.filter(
        active=True), "title": "Active Listings"}
    return render(request, "auctions/index.html", context)


def watchlist_view(request):
    """
    Renders the watchlist page for the logged in user.

    Parameters:
        request (HttpRequest): The request instance.

    Returns:
        HttpResponse: The response instance, rendering the index page template with all watchlisted listings.
    """
    context = {"listings": request.user.watchlist.all(), "title": "Watchlist"}
    return render(request, "auctions/index.html", context)


def categories_list(request):
    """
    Renders the list of categories from Listing.CATEGORIES_CHOICES.

    Parameters:
        request (HttpRequest): The request instance.

    Returns:
        HttpResponse: The response instance, rendering the categories template with links to all category pages.
    """
    categories = Listing.CATEGORIES_CHOICES
    context = {"categories": categories}
    return render(request, "auctions/categories.html", context)


def category_view(request, category):
    """
    Renders the listings in a specific category.

    Parameters:
        request (HttpRequest): The request instance.
        category(string): Human-readable name of the category

    Returns:
        HttpResponse: The response instance, rendering the listings inside a specific category.
    """
    for choice in Listing.CATEGORIES_CHOICES:
        if category.replace("-", " ") == choice[1]:
            category = choice[0]
            break
    context = {"listings": Listing.objects.filter(category=category)}
    return render(request, "auctions/index.html", context)


def listing(request, id, url):
    """
    Renders the listing page for any listing on the homepage, and also renders the NewBidForm.

    Parameters:
        request (HttpRequest): The request instance.
        id (int): The id of the listing to be rendered.
        url (string): The formatted title of the listing to be shown in the URL for that listing.

    Returns:
        HttpResponse: The response instance, rendering the listing page for a specific listing.
    """
    listing = Listing.objects.get(pk=id)
    bids = Bid.objects.filter(listing_id=id)

    # Get the minimum bid value
    if bids:
        min_value = bids.last().bid
    else:
        min_value = listing.start_bid

    # Handle the new bid submission
    if request.method == "POST":
        form = BidForm(request.POST, min_value=min_value)
        if form.is_valid():
            new_bid = form.cleaned_data["new_bid"]
            new_bid = Bid(user=request.user, listing=listing, bid=new_bid)
            new_bid.save()
            return redirect('listing', id=listing.id, url=url)
    else:
        form = BidForm(min_value=min_value)

    context = {"listing": listing, "bids": bids, "bid_form": form}
    return render(request, "auctions/listing.html", context)


def watchlist(request, id, url):
    """
    Handles adding or removing Listing from User's watchlist.

    Parameters:
        request (HttpRequest): The request instance.
        id (int): The id of the listing for redirect.
        url (string): The formatted title of the listing to be shown in the URL for that listing.

    Returns:
        HttpResponse: The response instance, redirecting back to the listing page after adding it to watchlist.
    """
    listing = Listing.objects.get(pk=id)

    # If listing is already watchlisted, remove it from watchlist, else add to the watchlist
    if listing in request.user.watchlist.all():
        (request.user).watchlist.remove(listing)
    else:
        (request.user).watchlist.add(listing)
    return redirect('listing', id=listing.id, url=url)


def new_listing(request):
    """
    Renders the NewListingForm, and when submitted, creates a new listing and redirects to the homepage.

    Parameters:
        request (HttpRequest): The request instance.

    Returns:
        HttpResponse: The response instance, either rendering the form or redirecting to the homepage.
    """
    # Handle the form submission for a new listing, and add it to the database
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new = Listing(title=data["title"], description=data["description"], start_bid=data["start_bid"],
                          image=data["image"], category=data["category"], active=True, author=request.user)
            new.save()
            return redirect('index')
    else:
        form = NewListingForm

    context = {"listing_form": form}
    return render(request, "auctions/create.html", context)


def close_auction(request, id, url):
    """
    Makes the listing inactive and makes the last bidder the winner of the auction.

    Parameters:
        request (HttpRequest): The request instance.
        id (int): The id of the listing to be closed.
        url (string): The formatted title of the listing to be shown in the URL for that listing.

    Returns:
        HttpResponse: The response instance, rendering the updated page for the closed listing.
    """
    listing = Listing.objects.get(pk=id)
    listing.active = False

    # Determine the winner
    bids = Bid.objects.filter(listing_id=id)
    if (bids.last()):
        listing.winner = bids.last().user
    else:
        listing.winner = request.user

    listing.save()
    return redirect('listing', id=listing.id, url=url)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return redirect("index")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(  # type: ignore
                username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect("index")
    else:
        return render(request, "auctions/register.html")


@csrf_exempt
def comment(request, id, url):
    if request.method == 'POST':
        form = request.POST
        comment = form.get('comment')
        Comment(user=request.user, listing=Listing.objects.get(pk=id), comment=comment).save()
    return redirect('listing', id=id, url=url)
