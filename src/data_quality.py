import sys
import os
import mysql.connector
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

quality_failed = False


# MySQL connection
connection = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("Aarti@123"),
    database=os.getenv("MYSQL_DATABASE")
)

cursor = connection.cursor()


# --------------------------------------------------
# 1. Duplicate Ride Check
# --------------------------------------------------

print("\n--- Duplicate Ride Check ---")

cursor.execute("""
SELECT ride_id, COUNT(*)
FROM staging_rides
GROUP BY ride_id
HAVING COUNT(*) > 1
""")

duplicates = cursor.fetchall()

if duplicates:
    print("Duplicate rides found:")
    for row in duplicates:
        print(row)

    quality_failed = True

else:
    print("No duplicate rides found.")


# --------------------------------------------------
# 2. Invalid Driver Check
# --------------------------------------------------

print("\n--- Invalid Driver Check ---")

cursor.execute("""
SELECT r.ride_id, r.driver_id
FROM staging_rides r
LEFT JOIN staging_drivers d
ON r.driver_id = d.driver_id
WHERE d.driver_id IS NULL
""")

invalid_drivers = cursor.fetchall()

if invalid_drivers:
    print("Invalid driver references found:")

    for row in invalid_drivers:
        print(row)

    quality_failed = True

else:
    print("No invalid driver references found.")


# --------------------------------------------------
# 3. Invalid Customer Check
# --------------------------------------------------

print("\n--- Invalid Customer Check ---")

cursor.execute("""
SELECT r.ride_id, r.customer_id
FROM staging_rides r
LEFT JOIN staging_customers c
ON r.customer_id = c.customer_id
WHERE c.customer_id IS NULL
""")

invalid_customers = cursor.fetchall()

if invalid_customers:
    print("Invalid customer references found:")

    for row in invalid_customers:
        print(row)

    quality_failed = True

else:
    print("No invalid customer references found.")


# --------------------------------------------------
# 4. Negative Fare Check
# --------------------------------------------------

print("\n--- Negative Fare Check ---")

cursor.execute("""
SELECT ride_id, fare
FROM staging_rides
WHERE fare < 0
""")

negative_fares = cursor.fetchall()

if negative_fares:
    print("Negative fares found:")

    for row in negative_fares:
        print(row)

    quality_failed = True

else:
    print("No negative fares found.")


# --------------------------------------------------
# 5. Rating Validation
# --------------------------------------------------

print("\n--- Rating Validation ---")

cursor.execute("""
SELECT ride_id, rating
FROM staging_rides
WHERE rating IS NOT NULL
AND (rating < 1 OR rating > 5)
""")

invalid_ratings = cursor.fetchall()

if invalid_ratings:
    print("Invalid ratings found:")

    for row in invalid_ratings:
        print(row)

    quality_failed = True

else:
    print("No invalid ratings found.")


# --------------------------------------------------
# 6. Payment Reference Check
# --------------------------------------------------

print("\n--- Payment Reference Check ---")

cursor.execute("""
SELECT p.payment_id, p.ride_id
FROM staging_payments p
LEFT JOIN staging_rides r
ON p.ride_id = r.ride_id
WHERE r.ride_id IS NULL
""")

invalid_payments = cursor.fetchall()

if invalid_payments:
    print("Payments with invalid ride references found:")

    for row in invalid_payments:
        print(row)

    quality_failed = True

else:
    print("No invalid payment references found.")


# --------------------------------------------------
# Close database connection
# --------------------------------------------------

cursor.close()
connection.close()


# --------------------------------------------------
# Final Data Quality Result
# --------------------------------------------------

if quality_failed:

    print("\n❌ DATA QUALITY CHECKS FAILED")
    print("Pipeline should stop before transformation.")

    sys.exit(1)

else:

    print("\n✅ ALL DATA QUALITY CHECKS PASSED")

    sys.exit(0)