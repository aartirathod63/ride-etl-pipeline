import mysql.connector

from extract import read_csv


# -----------------------------
# MYSQL CONNECTION
# -----------------------------

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Aarti@123",
    database="ride_analytics_db"
)

cursor = connection.cursor()


# -----------------------------
# CLEAR OLD STAGING DATA
# -----------------------------

cursor.execute("TRUNCATE TABLE staging_customers")
cursor.execute("TRUNCATE TABLE staging_drivers")
cursor.execute("TRUNCATE TABLE staging_rides")
cursor.execute("TRUNCATE TABLE staging_payments")


# -----------------------------
# EXTRACT CSV DATA
# -----------------------------

customers = read_csv("data/customers.csv")
drivers = read_csv("data/drivers.csv")
rides = read_csv("data/rides.csv")
payments = read_csv("data/payments.csv")


# -----------------------------
# LOAD CUSTOMERS
# -----------------------------

customer_query = """
INSERT INTO staging_customers
(
    customer_id,
    customer_name,
    city,
    signup_date
)
VALUES (%s, %s, %s, %s)
"""

customer_values = [
    (
        row["customer_id"],
        row["customer_name"],
        row["city"],
        row["signup_date"]
    )
    for row in customers
]

cursor.executemany(customer_query, customer_values)


# -----------------------------
# LOAD DRIVERS
# -----------------------------

driver_query = """
INSERT INTO staging_drivers
(
    driver_id,
    driver_name,
    city,
    vehicle_type
)
VALUES (%s, %s, %s, %s)
"""

driver_values = [
    (
        row["driver_id"],
        row["driver_name"],
        row["city"],
        row["vehicle_type"]
    )
    for row in drivers
]

cursor.executemany(driver_query, driver_values)


# -----------------------------
# LOAD RIDES
# -----------------------------

ride_query = """
INSERT INTO staging_rides
(
    ride_id,
    customer_id,
    driver_id,
    ride_date,
    pickup_city,
    drop_city,
    distance_km,
    fare,
    status,
    rating
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

ride_values = [
    (
        row["ride_id"],
        row["customer_id"],
        row["driver_id"],
        row["ride_date"],
        row["pickup_city"],
        row["drop_city"],
        row["distance_km"],
        row["fare"],
        row["status"],
        row["rating"] if row["rating"] else None
    )
    for row in rides
]

cursor.executemany(ride_query, ride_values)


# -----------------------------
# LOAD PAYMENTS
# -----------------------------

payment_query = """
INSERT INTO staging_payments
(
    payment_id,
    ride_id,
    payment_method,
    amount,
    payment_status
)
VALUES (%s, %s, %s, %s, %s)
"""

payment_values = [
    (
        row["payment_id"],
        row["ride_id"],
        row["payment_method"],
        row["amount"],
        row["payment_status"]
    )
    for row in payments
]

cursor.executemany(payment_query, payment_values)


# -----------------------------
# COMMIT TRANSACTION
# -----------------------------

connection.commit()


print("Customers loaded successfully!")
print("Drivers loaded successfully!")
print("Rides loaded successfully!")
print("Payments loaded successfully!")


# -----------------------------
# CLOSE CONNECTION
# -----------------------------

cursor.close()
connection.close()