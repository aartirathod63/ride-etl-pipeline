import csv
import random
from datetime import datetime, timedelta

random.seed(42)

cities = ["Pune", "Mumbai", "Bengaluru", "Delhi", "Hyderabad"]

first_names = [
    "Aarav", "Riya", "Neha", "Kabir", "Sneha",
    "Rahul", "Ananya", "Vikram", "Priya", "Karan"
]

last_names = [
    "Sharma", "Patil", "Joshi", "Singh", "Kulkarni",
    "Mehta", "Deshmukh", "Rao", "Shah", "Gupta"
]

vehicle_types = ["Sedan", "SUV", "Hatchback"]

payment_methods = ["UPI", "Card", "Cash", "Wallet"]

ride_statuses = ["Completed", "Completed", "Completed", "Cancelled"]


# -----------------------------
# CUSTOMERS
# -----------------------------

customers = []

for i in range(1, 21):

    customers.append({
        "customer_id": f"C{i:03}",
        "customer_name": f"{random.choice(first_names)} {random.choice(last_names)}",
        "city": random.choice(cities),
        "signup_date": (
            datetime(2025, 1, 1)
            + timedelta(days=random.randint(0, 100))
        ).date()
    })


# -----------------------------
# DRIVERS
# -----------------------------

drivers = []

for i in range(1, 11):

    drivers.append({
        "driver_id": f"D{i:03}",
        "driver_name": f"{random.choice(first_names)} {random.choice(last_names)}",
        "city": random.choice(cities),
        "vehicle_type": random.choice(vehicle_types)
    })


# -----------------------------
# RIDES
# -----------------------------

rides = []

for i in range(1, 101):

    distance = round(random.uniform(2, 25), 2)

    status = random.choice(ride_statuses)

    if status == "Completed":
        fare = round(distance * random.uniform(20, 35), 2)
        rating = random.randint(1, 5)
    else:
        fare = 0
        rating = None

    ride_date = (
        datetime(2025, 3, 1)
        + timedelta(days=random.randint(0, 30))
    ).date()

    rides.append({
        "ride_id": f"R{i:04}",
        "customer_id": random.choice(customers)["customer_id"],
        "driver_id": random.choice(drivers)["driver_id"],
        "ride_date": ride_date,
        "pickup_city": random.choice(cities),
        "drop_city": random.choice(cities),
        "distance_km": distance,
        "fare": fare,
        "status": status,
        "rating": rating
    })


# -----------------------------
# PAYMENTS
# -----------------------------

payments = []

for i, ride in enumerate(rides, start=1):

    if ride["status"] == "Completed":

        payment_status = "Success"
        amount = ride["fare"]

    else:

        payment_status = "Failed"
        amount = 0

    payments.append({
        "payment_id": f"P{i:04}",
        "ride_id": ride["ride_id"],
        "payment_method": random.choice(payment_methods),
        "amount": amount,
        "payment_status": payment_status
    })


# -----------------------------
# WRITE CSV FILES
# -----------------------------

def write_csv(filename, rows):

    if not rows:
        return

    with open(filename, "w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=rows[0].keys()
        )

        writer.writeheader()
        writer.writerows(rows)


write_csv("data/customers.csv", customers)
write_csv("data/drivers.csv", drivers)
write_csv("data/rides.csv", rides)
write_csv("data/payments.csv", payments)

print("Data generation completed successfully!")