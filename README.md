# Falcons Sports Club -- Sign-up Funnel Analytics

## Project Overview

This project creates a simulated dataset for the Falcons Sports Club
sign-up funnel. It is designed to help analyze how visitors move through
the registration and membership process and identify where users leave
the funnel.

The dataset contains **1,000 simulated users** and an event log stored
in a SQLite database.

## Project Objectives

-   Generate realistic sample user and event data.
-   Track the main stages of the sign-up funnel.
-   Create a deliberate verification drop-off pattern for analysis.
-   Store the generated data in a relational SQLite database.
-   Support funnel KPI analysis using SQL and BI tools.

## Tools and Technologies

-   Python
-   Pandas
-   NumPy
-   SQLite
-   SQL

## Project Files

  -----------------------------------------------------------------------
  File                                Description
  ----------------------------------- -----------------------------------
  `generate_data.py`                  Python script that generates the
                                      simulated data and creates the
                                      SQLite database.

  `falcons.db`                        SQLite database containing the
                                      `users` and `events` tables.

  `README.md`                         Project overview and instructions.
  -----------------------------------------------------------------------

## Database Structure

The database is named `falcons.db` and contains two tables.

### 1. `users`

One row represents one registered user.

  -----------------------------------------------------------------------
  Column                              Description
  ----------------------------------- -----------------------------------
  `user_id`                           Unique user identifier and primary
                                      key.

  `full_name`                         User's simulated full name.

  `email`                             Unique simulated email address.

  `phone_number`                      Simulated phone number.

  `signup_date`                       Date and time when the user
                                      completed signup.

  `is_verified`                       Whether the user completed email
                                      verification (0/1 in SQLite).

  `verified_at`                       Verification timestamp; NULL if not
                                      verified.

  `membership_plan`                   Monthly, quarterly, or yearly plan.

  `payment_date`                      Payment timestamp; NULL if no
                                      payment.

  `payment_amount`                    Membership payment amount.

  `activated_at`                      First check-in / activation
                                      timestamp; NULL if not activated.

  `traffic_source`                    Acquisition source, such as
                                      organic, Facebook, Instagram,
                                      Google Ads, or referral.

  `is_test_account`                   Indicates whether the record is a
                                      test account (0/1 in SQLite).
  -----------------------------------------------------------------------

### 2. `events`

One row represents one recorded user action.

  -----------------------------------------------------------------------
  Column                              Description
  ----------------------------------- -----------------------------------
  `event_id`                          Unique event identifier and primary
                                      key.

  `session_id`                        Identifier for the session in which
                                      the event occurred.

  `user_id`                           Related user identifier; NULL for
                                      anonymous pre-signup events.

  `event_type`                        Name of the recorded action.

  `event_timestamp`                   Date and time when the event
                                      occurred.

  `page_url`                          Page associated with the event,
                                      when applicable.

  `device_type`                       Mobile, desktop, or tablet, when
                                      applicable.

  `traffic_source`                    Acquisition source, when
                                      applicable.

  `event_value`                       Event value, used for the payment
                                      amount on completed payments.
  -----------------------------------------------------------------------

The relationship is **one user to many events**. The `events.user_id`
field references `users.user_id`. Anonymous events before signup can
have a NULL `user_id`.

## Funnel Stages and Event Types

The funnel is represented by these events:

1.  **Visit** -- `page_view`
2.  **Signup started** -- `signup_started`
3.  **Signup completed** -- `signup_completed`
4.  **Verification completed** -- `email_verified`
5.  **Payment started** -- `payment_started`
6.  **Payment completed** -- `payment_completed`
7.  **Activation** -- `first_checkin`

## Data Generation

The `generate_data.py` script creates the simulated dataset and saves it
to `falcons.db`.

The script:

1.  Sets random seeds to make the generated data reproducible.
2.  Generates 1,000 simulated users with signup dates between October 1,
    2026 and November 20, 2026.
3.  Assigns user details, traffic sources, and device types.
4.  Plants a verification drop-off pattern: exactly 40% of users do not
    complete email verification.
5.  Generates later verification, payment, and activation events for
    users who progress through the funnel.
6.  Creates the SQLite tables and inserts the generated records.
7.  Prints validation counts and the verification drop-off percentage.

### Planted Verification Drop-off

The simulation deliberately sets:

-   Total signups: **1,000**
-   Verified users: **600**
-   Unverified users: **400**
-   Verification drop-off: **40%**

This pattern is intentional and provides a clear funnel drop-off point
for analysis. Payment and activation outcomes are generated
probabilistically, so their counts can vary if the generation logic or
random seed changes.

## How to Run

Make sure Python and the required packages are installed.

Install dependencies if needed:

``` bash
pip install pandas numpy
```

Run the data-generation script from the project folder:

``` bash
python generate_data.py
```

The script creates or replaces `falcons.db` in the same folder. It
recreates the `users` and `events` tables each time it runs, so existing
contents of those tables are replaced.

## Validation

After running the script, the terminal should display summary
information including:

-   Total users
-   Total events
-   Verified users
-   Verification drop-off count
-   Verification drop-off percentage

The generated database can also be checked with SQL:

``` sql
SELECT COUNT(*) AS total_users
FROM users;

SELECT COUNT(*) AS total_events
FROM events;

SELECT COUNT(DISTINCT user_id) AS verified_users
FROM events
WHERE event_type = 'email_verified';
```

## KPI Definitions

The dataset supports analysis of these funnel KPIs:

  -----------------------------------------------------------------------
  KPI                                 Definition
  ----------------------------------- -----------------------------------
  Visitor-to-Signup Conversion        Unique visitors who complete signup
                                      divided by unique visitors.

  Signup-to-Verification Rate         Unique users who verify email
                                      divided by users who complete
                                      signup.

  Verified-to-Paid Conversion         Verified users who complete payment
                                      divided by verified users.

  Payment-to-Activation Rate          Users who complete first check-in
                                      divided by users who complete
                                      payment.

  Overall Visitor-to-Paid Conversion  Unique visitors who complete
                                      payment divided by unique visitors.
  -----------------------------------------------------------------------

For visitor counts, use distinct `session_id` values from `page_view`
events. For signup and later funnel stages, use distinct `user_id`
values for the relevant event types. Exclude test accounts
(`is_test_account = 1`) from user-based KPI calculations. Use the same
cohort period and counting rules when comparing KPIs.

## Notes and Assumptions

-   This is simulated data, not real customer information.
-   Dates are generated as naive Python datetimes and are intended to
    represent UTC timestamps.
-   SQLite stores Boolean values as integers (0 and 1).
-   Missing or not-applicable values are stored as NULL.
-   The event type `email_verified` is used consistently with the
    project data dictionary.
-   The generated event count depends on the number of users progressing
    to payment and activation.

## Future Work

-   Write SQL queries to calculate the five funnel KPIs.
-   Analyze conversion and drop-off by traffic source and device type.
-   Build a dashboard in Power BI or Tableau.
-   Identify opportunities to improve the verification step.
