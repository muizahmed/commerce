# Auction Site Project

Implementation of an auction site as part of the CS50W course. Django is used for the backend, including models for AuctionListing, Bid, and Comment. Frontend modifications are focused on enhancing the user interface.

## Demo
[]

## Features

- **Create Listing:** Users can create new listings with a title, description, starting bid, optional image URL, and category.
- **Active Listings Page:** Default route displays all active auction listings, showing title, description, current price, and photo (if available).
- **Listing Page:** Clicking on a listing reveals all details, allowing users to add the item to their Watchlist, bid, or close the auction (if they created it).
- **Watchlist:** Signed-in users can view and manage listings they've added to their Watchlist.
- **Categories:** Users can explore active listings categorized by type.
- **Django Admin Interface:** Administrators can manage listings, comments, and bids via the Django admin interface.

## Usage

1. Clone the repository: `git clone https://github.com/your-username/auction-site.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Use superuser `admin` with password `admin`
5. Start the development server: `python manage.py runserver`
6. Access the site at `http://127.0.0.1:8000/` and the admin interface at `http://127.0.0.1:8000/admin/`

## Credits

- [CS50W OpenWare](https://cs50.harvard.edu/web/2020/projects/2/commerce/)
