import sqlite3

# SQLite database file (created automatically if it doesn't exist)
DB_FILE = "flights.db"


def get_connection():
    """Return a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Rows behave like dicts
    return conn


def init_db():
    """Create the tracked_flights table if it doesn't already exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tracked_flights (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            from_airport TEXT NOT NULL,
            to_airport   TEXT NOT NULL,
            travel_date  TEXT NOT NULL,
            email        TEXT NOT NULL,
            target_price REAL,           -- optional: user's desired max price
            last_price   REAL,           -- most recent price fetched
            lowest_price REAL,           -- lowest price seen so far
            created_at   TEXT DEFAULT (datetime('now'))
        )
    """)

    conn.commit()
    conn.close()
    print("Database initialized.")


def save_flight(from_airport, to_airport, travel_date, email, target_price, price):
    """Insert a new tracked flight into the database."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tracked_flights
            (from_airport, to_airport, travel_date, email, target_price, last_price, lowest_price)
        VALUES
            (?, ?, ?, ?, ?, ?, ?)
    """, (
        from_airport.upper(),
        to_airport.upper(),
        travel_date,
        email,
        target_price,
        price,   # last_price = initial fetch
        price    # lowest_price = same on first save
    ))

    conn.commit()
    conn.close()


def get_all_flights():
    """Fetch all tracked flights (used by the daily scheduler)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tracked_flights")
    rows = cursor.fetchall()
    conn.close()
    return rows


def update_prices(flight_id, new_price, new_lowest):
    """Update last_price and lowest_price for a flight after a daily check."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tracked_flights
        SET last_price = ?, lowest_price = ?
        WHERE id = ?
    """, (new_price, new_lowest, flight_id))

    conn.commit()
    conn.close()
