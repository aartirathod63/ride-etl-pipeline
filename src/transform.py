import mysql.connector


connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Aarti@123",
    database="ride_analytics_db"
)

cursor = connection.cursor()


# Clear existing analytics data
cursor.execute("TRUNCATE TABLE ride_analytics")


# Transformation query
transform_query = """
INSERT INTO ride_analytics
(
    ride_id,
    customer_id,
    customer_name,
    driver_id,
    driver_name,
    ride_date,
    pickup_city,
    drop_city,
    distance_km,
    fare,
    ride_status,
    rating,
    payment_method,
    payment_status,
    revenue_category
)

SELECT
    r.ride_id,
    r.customer_id,
    c.customer_name,
    r.driver_id,
    d.driver_name,
    r.ride_date,
    r.pickup_city,
    r.drop_city,
    r.distance_km,
    r.fare,
    r.status,
    r.rating,
    p.payment_method,
    p.payment_status,

    CASE
        WHEN r.fare >= 1000 THEN 'HIGH'
        WHEN r.fare >= 500 THEN 'MEDIUM'
        ELSE 'LOW'
    END

FROM staging_rides r

LEFT JOIN staging_customers c
    ON r.customer_id = c.customer_id

LEFT JOIN staging_drivers d
    ON r.driver_id = d.driver_id

LEFT JOIN staging_payments p
    ON r.ride_id = p.ride_id
"""


cursor.execute(transform_query)

connection.commit()


# Verify number of transformed records
cursor.execute("SELECT COUNT(*) FROM ride_analytics")

count = cursor.fetchone()[0]

print(f"Transformation completed successfully!")
print(f"Records in ride_analytics: {count}")


cursor.close()
connection.close()