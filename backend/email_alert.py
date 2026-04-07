import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load .env so EMAIL and EMAIL_PASSWORD are available via os.getenv
load_dotenv()


def send_email(to_email, subject, body):
    """
    Send an email via Gmail SMTP.

    Credentials are loaded from .env:
      EMAIL          — your Gmail address
      EMAIL_PASSWORD — your Gmail App Password (not your real password)
    """
    sender = os.getenv("EMAIL")
    password = os.getenv("EMAIL_PASSWORD")

    # Guard: skip silently if credentials are missing (e.g. during local dev)
    if not sender or not password:
        print("[email] WARNING: EMAIL or EMAIL_PASSWORD not set in .env — skipping.")
        return

    # Build the email message
    msg = MIMEMultipart()
    msg["From"]    = sender
    msg["To"]      = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    print(f"[email] Sending '{subject}' to {to_email}...")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()      # identify to the server
            server.starttls()  # upgrade to TLS encrypted connection
            server.login(sender, password)
            server.sendmail(sender, to_email, msg.as_string())
        print(f"[email] Sent successfully to {to_email}")

    except smtplib.SMTPAuthenticationError:
        print("[email] ERROR: Authentication failed. Check EMAIL and EMAIL_PASSWORD in .env.")
        print("[email] Tip: Use a Gmail App Password, not your account password.")

    except smtplib.SMTPConnectError:
        print("[email] ERROR: Could not connect to smtp.gmail.com:587. Check your internet connection.")

    except smtplib.SMTPRecipientsRefused:
        print(f"[email] ERROR: Recipient address rejected by server: {to_email}")

    except Exception as e:
        # Catch-all — log the error type and message without crashing the app
        print(f"[email] ERROR: Unexpected error sending email: {type(e).__name__}: {e}")


# ─── Email templates ──────────────────────────────────────────────────────────

def send_tracking_started(to_email, from_airport, to_airport, travel_date, price):
    """Email sent immediately when a user starts tracking a flight."""
    subject = f"✈ Tracking started: {from_airport} → {to_airport}"
    body = f"""Hi,

You've started tracking flight prices for:

  Route : {from_airport} → {to_airport}
  Date  : {travel_date}
  Price : ${price:.2f} (current price at time of signup)

We'll check prices daily and alert you if anything changes.

Alert types you may receive:
  - Price dropped
  - New lowest price ever
  - Price increased
  - 1-week reminder before your travel date

Stay tuned!

— Flight Price Tracker
"""
    send_email(to_email, subject, body)


def send_price_drop(to_email, from_airport, to_airport, travel_date, old_price, new_price):
    """Email sent when today's price is lower than yesterday's."""
    subject = f"Price dropped: {from_airport} → {to_airport}"
    body = f"""Good news!

The price for your tracked flight has dropped:

  Route     : {from_airport} → {to_airport}
  Date      : {travel_date}
  Old price : ${old_price:.2f}
  New price : ${new_price:.2f}
  You save  : ${old_price - new_price:.2f}

Book now before it goes back up!

— Flight Price Tracker
"""
    send_email(to_email, subject, body)


def send_lowest_price(to_email, from_airport, to_airport, travel_date, price):
    """Email sent when today's price is the lowest ever seen."""
    subject = f"Lowest price ever: {from_airport} → {to_airport}"
    body = f"""Lowest price alert!

We found the lowest price ever for your tracked flight:

  Route        : {from_airport} → {to_airport}
  Date         : {travel_date}
  Lowest price : ${price:.2f}

This is the best price we've seen. Consider booking now!

— Flight Price Tracker
"""
    send_email(to_email, subject, body)


def send_price_increase(to_email, from_airport, to_airport, travel_date, old_price, new_price):
    """Email sent when today's price is higher than yesterday's."""
    subject = f"Price increased: {from_airport} → {to_airport}"
    body = f"""Heads up!

The price for your tracked flight has increased:

  Route     : {from_airport} → {to_airport}
  Date      : {travel_date}
  Old price : ${old_price:.2f}
  New price : ${new_price:.2f}

Prices may continue to rise. Stay alert for future drops.

— Flight Price Tracker
"""
    send_email(to_email, subject, body)


def send_reminder(to_email, from_airport, to_airport, travel_date, price):
    """Email sent 7 days before travel date."""
    subject = f"1-week reminder: {from_airport} → {to_airport}"
    body = f"""Reminder!

Your tracked flight is one week away:

  Route         : {from_airport} → {to_airport}
  Date          : {travel_date}
  Current price : ${price:.2f}

If you haven't booked yet, now is a good time!

— Flight Price Tracker
"""
    send_email(to_email, subject, body)
