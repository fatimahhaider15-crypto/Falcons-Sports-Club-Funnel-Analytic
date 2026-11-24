
import pandas as pd
import numpy as np
import random
import sqlite3
from datetime import datetime, timedelta

# 1. Set random seeds for reproducible data
random.seed(42)
np.random.seed(42)

TOTAL_USERS = 1000

user_ids = list(range(1001, 1001 + TOTAL_USERS))

first_names = [
    "Ali", "Sara", "Ahmed", "Fatima", "Bilal",
    "Ayesha", "Usman", "Hira", "Hamza", "Zain",
    "Maryam", "Saad", "Iqra", "Daniyal", "Sana",
    "Hassan", "Mahnoor", "Omar", "Noor", "Khan"
]

last_names = [
    "Khan", "Ahmed", "Raza", "Malik", "Shah",
    "Ali", "Hussain", "Siddiqui", "Abbasi", "Akhtar"
]

traffic_sources = [
    "organic", "facebook", "instagram",
    "google_ads", "referral"
]

device_types = ["mobile", "desktop", "tablet"]
membership_plans = ["monthly", "quarterly", "yearly"]

# 2. Generate user information
full_names = [
    random.choice(first_names) + " " + random.choice(last_names)
    for _ in range(TOTAL_USERS)
]

emails = [
    f"user{user_id}@example.com"
    for user_id in user_ids
]

phone_numbers = [
    f"+923000{user_id:07d}"
    for user_id in user_ids
]

start_date = datetime(2026, 10, 1)
end_date = datetime(2026, 11, 20)

signup_dates = [
    start_date + timedelta(
        seconds=random.randint(
            0,
            int((end_date - start_date).total_seconds())
        )
    )
    for _ in range(TOTAL_USERS)
]

signup_dates = sorted(signup_dates)

# 3. Plant the 40% verification drop-off pattern
dropoff_count = int(TOTAL_USERS * 0.40)
unverified_indices = set(
    random.sample(range(TOTAL_USERS), dropoff_count)
)

is_verified = [
    i not in unverified_indices
    for i in range(TOTAL_USERS)
]

verified_at = []
membership_plan_values = []
payment_dates = []
payment_amounts = []
activated_at = []

plan_prices = {
    "monthly": 5000,
    "quarterly": 13500,
    "yearly": 48000
}

# 4. Generate verification, payment and activation data
for i in range(TOTAL_USERS):

    if is_verified[i]:

        verification_time = signup_dates[i] + timedelta(
            minutes=random.randint(2, 60)
        )
        verified_at.append(verification_time)

        if random.random() < 0.60:

            plan = random.choice(membership_plans)

            payment_time = verification_time + timedelta(
                hours=random.randint(1, 72)
            )

            amount = plan_prices[plan]

            if random.random() < 0.80:
                activation_time = payment_time + timedelta(
                    days=random.randint(1, 7)
                )
            else:
                activation_time = None

            membership_plan_values.append(plan)
            payment_dates.append(payment_time)
            payment_amounts.append(amount)
            activated_at.append(activation_time)

        else:
            membership_plan_values.append(None)
            payment_dates.append(None)
            payment_amounts.append(None)
            activated_at.append(None)

    else:
        verified_at.append(None)
        membership_plan_values.append(None)
        payment_dates.append(None)
        payment_amounts.append(None)
        activated_at.append(None)

# 5. Create users DataFrame
users_df = pd.DataFrame({
    "user_id": user_ids,
    "full_name": full_names,
    "email": emails,
    "phone_number": phone_numbers,
    "signup_date": signup_dates,
    "is_verified": is_verified,
    "verified_at": verified_at,
    "membership_plan": membership_plan_values,
    "payment_date": payment_dates,
    "payment_amount": payment_amounts,
    "activated_at": activated_at,
    "traffic_source": [
        random.choice(traffic_sources)
        for _ in range(TOTAL_USERS)
    ],
    "is_test_account": [False] * TOTAL_USERS
})

# 6. Generate events
events = []
event_id = 900001

for i in range(TOTAL_USERS):

    user_id = user_ids[i]
    signup_time = signup_dates[i]
    source = users_df.loc[i, "traffic_source"]
    device = random.choice(device_types)

    session_id = f"sess_{user_id}_01"

    # Anonymous page visit
    events.append({
        "event_id": event_id,
        "session_id": session_id,
        "user_id": None,
        "event_type": "page_view",
        "event_timestamp": signup_time - timedelta(minutes=5),
        "page_url": "/home",
        "device_type": device,
        "traffic_source": source,
        "event_value": None
    })
    event_id += 1

    # Signup started
    events.append({
        "event_id": event_id,
        "session_id": session_id,
        "user_id": None,
        "event_type": "signup_started",
        "event_timestamp": signup_time - timedelta(minutes=2),
        "page_url": "/signup",
        "device_type": device,
        "traffic_source": source,
        "event_value": None
    })
    event_id += 1

    # Signup completed
    events.append({
        "event_id": event_id,
        "session_id": session_id,
        "user_id": user_id,
        "event_type": "signup_completed",
        "event_timestamp": signup_time,
        "page_url": "/signup",
        "device_type": device,
        "traffic_source": source,
        "event_value": None
    })
    event_id += 1

    if users_df.loc[i, "is_verified"]:

        verification_time = users_df.loc[i, "verified_at"]
        verify_session = f"sess_{user_id}_02"

        events.append({
            "event_id": event_id,
            "session_id": verify_session,
            "user_id": user_id,
            "event_type": "email_verified",
            "event_timestamp": verification_time,
            "page_url": "/verify",
            "device_type": device,
            "traffic_source": source,
            "event_value": None
        })
        event_id += 1

        if pd.notna(users_df.loc[i, "payment_date"]):

            payment_time = users_df.loc[i, "payment_date"]
            payment_session = f"sess_{user_id}_03"

            events.append({
                "event_id": event_id,
                "session_id": payment_session,
                "user_id": user_id,
                "event_type": "payment_started",
                "event_timestamp": payment_time - timedelta(minutes=10),
                "page_url": "/checkout",
                "device_type": device,
                "traffic_source": source,
                "event_value": None
            })
            event_id += 1

            events.append({
                "event_id": event_id,
                "session_id": payment_session,
                "user_id": user_id,
                "event_type": "payment_completed",
                "event_timestamp": payment_time,
                "page_url": "/checkout",
                "device_type": device,
                "traffic_source": source,
                "event_value": users_df.loc[i, "payment_amount"]
            })
            event_id += 1

            if pd.notna(users_df.loc[i, "activated_at"]):

                events.append({
                    "event_id": event_id,
                    "session_id": f"sess_{user_id}_04",
                    "user_id": user_id,
                    "event_type": "first_checkin",
                    "event_timestamp": users_df.loc[i, "activated_at"],
                    "page_url": None,
                    "device_type": None,
                    "traffic_source": None,
                    "event_value": None
                })
                event_id += 1

events_df = pd.DataFrame(events)

events_df = events_df.sort_values(
    "event_timestamp"
).reset_index(drop=True)

# 7. Create SQLite database and tables
conn = sqlite3.connect("falcons.db")
conn.execute("PRAGMA foreign_keys = ON")

# Drop old tables so rerunning the script does not duplicate records
conn.execute("DROP TABLE IF EXISTS events")
conn.execute("DROP TABLE IF EXISTS users")

conn.execute("""
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone_number TEXT,
    signup_date TEXT NOT NULL,
    is_verified INTEGER NOT NULL,
    verified_at TEXT,
    membership_plan TEXT,
    payment_date TEXT,
    payment_amount REAL,
    activated_at TEXT,
    traffic_source TEXT,
    is_test_account INTEGER NOT NULL
)
""")

conn.execute("""
CREATE TABLE events (
    event_id INTEGER PRIMARY KEY,
    session_id TEXT NOT NULL,
    user_id INTEGER,
    event_type TEXT NOT NULL,
    event_timestamp TEXT NOT NULL,
    page_url TEXT,
    device_type TEXT,
    traffic_source TEXT,
    event_value REAL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

# 8. Insert data into SQLite
users_df.to_sql(
    "users", conn, if_exists="append", index=False
)

events_df.to_sql(
    "events", conn, if_exists="append", index=False
)

# 9. Validate database
total_users = pd.read_sql_query(
    "SELECT COUNT(*) AS total FROM users", conn
).iloc[0, 0]

total_events = pd.read_sql_query(
    "SELECT COUNT(*) AS total FROM events", conn
).iloc[0, 0]

verified_users = pd.read_sql_query("""
    SELECT COUNT(DISTINCT user_id) AS total
    FROM events
    WHERE event_type = 'email_verified'
""", conn).iloc[0, 0]

total_signups = pd.read_sql_query("""
    SELECT COUNT(DISTINCT user_id) AS total
    FROM events
    WHERE event_type = 'signup_completed'
""", conn).iloc[0, 0]

dropoff = total_signups - verified_users
dropoff_percentage = (dropoff / total_signups) * 100

conn.close()

# 10. Display final results
print("Falcons Sports Club data generated successfully!")
print("Total users:", total_users)
print("Total events:", total_events)
print("Verified users:", verified_users)
print("Verification drop-off:", dropoff)
print("Drop-off percentage:", dropoff_percentage, "%")
print("Database created: falcons.db")
