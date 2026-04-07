from datetime import date, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

from database import get_all_flights, update_prices
from email_alert import (
    send_price_drop,
    send_lowest_price,
    send_price_increase,
    send_reminder,
)


def get_mock_price():
    """
    Returns a mock price simulating a daily price change.
    TODO: Replace with real Amadeus API call in Step 5.
    """
    import random
    # Randomly fluctuate between $250 and $400 to simulate real price changes
    return round(random.uniform(250, 400), 2)


def check_prices():
    """
    Daily job: checks price for every tracked flight and sends alerts.
    Runs once per day via APScheduler.
    """
    print("Running daily price check...")
    flights = get_all_flights()

    if not flights:
        print("No tracked flights found.")
        return

    for flight in flights:
        try:
            flight_id    = flight["id"]
            from_airport = flight["from_airport"]
            to_airport   = flight["to_airport"]
            travel_date  = flight["travel_date"]
            email        = flight["email"]
            last_price   = flight["last_price"]
            lowest_price = flight["lowest_price"]

            # Get today's price
            new_price = get_mock_price()

            print(f"  {from_airport}→{to_airport} | last=${last_price} | new=${new_price}")

            # Determine new lowest price
            new_lowest = min(lowest_price, new_price)

            # ── Send the right alert ──────────────────────────────────────────

            if new_price < lowest_price:
                # Best price ever seen — takes priority over a regular drop
                send_lowest_price(email, from_airport, to_airport, travel_date, new_price)

            elif new_price < last_price:
                # Price dropped since yesterday
                send_price_drop(email, from_airport, to_airport, travel_date, last_price, new_price)

            elif new_price > last_price:
                # Price went up since yesterday
                send_price_increase(email, from_airport, to_airport, travel_date, last_price, new_price)

            # ── 1-week reminder (independent of price change) ─────────────────
            days_until_travel = (date.fromisoformat(travel_date) - date.today()).days
            if days_until_travel == 7:
                send_reminder(email, from_airport, to_airport, travel_date, new_price)

            # ── Update DB with today's price ──────────────────────────────────
            update_prices(flight_id, new_price, new_lowest)

        except Exception as e:
            # One failed flight should not stop the rest from being checked
            print(f"  Error checking flight {flight_id}: {e}")

    print("Daily price check complete.")


def start_scheduler():
    """
    Creates and starts the APScheduler background scheduler.
    Called once at app startup.
    Runs check_prices() every day at 08:00 AM.
    """
    scheduler = BackgroundScheduler()

    # Run every day at 8:00 AM
    scheduler.add_job(check_prices, "cron", hour=8, minute=0)

    scheduler.start()
    print("Scheduler started — daily price check runs at 08:00 AM.")
    return scheduler
