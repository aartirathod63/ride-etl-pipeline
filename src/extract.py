import csv


def read_csv(file_path):
    """
    Read a CSV file and return a list of dictionaries.
    """

    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        data = list(reader)

    return data


if __name__ == "__main__":

    customers = read_csv("data/customers.csv")
    drivers = read_csv("data/drivers.csv")
    rides = read_csv("data/rides.csv")
    payments = read_csv("data/payments.csv")

    print("Customers:", len(customers))
    print("Drivers:", len(drivers))
    print("Rides:", len(rides))
    print("Payments:", len(payments))