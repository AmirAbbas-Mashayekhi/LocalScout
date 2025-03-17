from yelp_objects.yelp_tools import YelpClientWrapper, YelpBusinessSearcher
from emails.email_tools import EmailInitializer, EmailService, SMTPInitializer
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
from pathlib import Path
import dotenv
import argparse
import os

# Credentials
dotenv.load_dotenv()
API_KEY = os.getenv("YELP_FUSION_API")
sender = os.getenv("SENDER")
receiver = os.getenv("RECEIVER")
APP_PASSWORD = os.getenv("APP_PASSWORD")

yelp_client = YelpClientWrapper(
    url="businesses/search",
    api_key=API_KEY,
    limit=50,
    sort_by="review_count",
)


def find_best_business(
    yelp_client: YelpClientWrapper, term: str, location: str
) -> dict:
    yelp_searcher = YelpBusinessSearcher(yelp_client)

    businesses: list[dict] = yelp_searcher.search(location, term)
    businesses.sort(
        key=lambda business: (business["review_count"], business["rating"]),
        reverse=True,
    )
    best_business: dict = businesses[0]

    return best_business


def email_best_business(business: dict):
    message = MIMEMultipart()
    template = Template(Path("email_template.html").read_text())
    body = template.substitute(
        business_name=business["name"],
        review_count=business["review_count"],
        rating=business["rating"],
        address=" ".join(business["location"]["display_address"]),
        phone=business["display_phone"],
        image=business["image_url"],
    )
    email_info = EmailInitializer(
        message,
        MIMEText(body, "html"),
        "Your business/service search result on LocalScout!",
        sender,
        receiver,
    )
    smtp_info = SMTPInitializer(sender, APP_PASSWORD, receiver)
    email_sender = EmailService(email_info, smtp_info)
    email_sender.send_email()


if __name__ == "__main__":
    # Command-line Arguments
    parser = argparse.ArgumentParser(description="Search for Yelp Businesses.")
    parser.add_argument(
        "--location",
        type=str,
        required=True,
        help='Search location (e.g., "New York, NY")',
    )
    parser.add_argument(
        "--term",
        required=True,
        type=str,
        help='Search term (e.g., "coffee", "restaurants")',
    )
    args = parser.parse_args()

    # Resulting
    best_business = find_best_business(
        yelp_client=yelp_client, location=args.location, term=args.term
    )
    # TODO This is where you'd send that business to rabbit
    email_best_business(best_business)
