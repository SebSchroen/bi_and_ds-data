import csv
import os
from faker import Faker
import random
from datetime import datetime, timedelta

if not os.path.exists('example_data'):
    os.makedirs('example_data')


def generate_german_customer_data(fake, num_customers=10):
    german_customer_data = []
    genders = ['male'] * 45 + ['female'] * 45 + ['diverse'] * 10  # Gender distribution

    for _ in range(num_customers):
        gender = random.choice(genders)
        first_name = fake.first_name_male() if gender == 'male' else fake.first_name_female() if gender == 'female' else fake.first_name()
        last_name = fake.last_name()
        zip_code = fake.postcode()
        address = fake.street_address()
        email = fake.email()
        
        # Generate a realistic birth date between 18 and 70 years ago
        current_year = 2023  # You may need to update this with the current year
        max_birth_year = current_year - 18
        min_birth_year = max_birth_year - 70
        birth_year = random.randint(min_birth_year, max_birth_year)
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)  # Limited to 28 to avoid invalid dates
        birth_date = fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=70)

        customer_data = {
            "customer_id": fake.unique.random_number(digits=5),  # Unique customer ID
            "gender": gender,
            "first_name": first_name,
            "last_name": last_name,
            "zip_code": zip_code,
            "address": address,
            "email": email,
            "birth_date": birth_date,
            "age": current_year - birth_date.year
        }

        german_customer_data.append(customer_data)

    return german_customer_data

def generate_orders(fake, customers, num_orders_per_customer=10):
    orders = []

    for customer in customers:
        for order_id in range(1, num_orders_per_customer + 1):
            # Generate order amount with a positive correlation with the customer's age
            age = customer['age']
            min_order_amount = 10 + 0.5 * age  # Adjust the correlation as needed
            max_order_amount = 100 + 1.5 * age  # Adjust the correlation as needed
            order_amount = round(random.uniform(min_order_amount, max_order_amount), 2)

            # Generate order timestamp between 2020 and 2023
            order_time = fake.date_time_between_dates(
                datetime(2020, 1, 1, 0, 0, 0, 0),
                datetime(2023, 12, 31, 23, 59, 59, 999),
                tzinfo=None
            )

            # Weighted randomization for order submission time
            if random.random() < 0.7:  # 70% chance of being between 4 pm and 8 pm
                order_time = order_time.replace(hour=random.randint(16, 20))
            else:
                order_time = order_time.replace(hour=random.randint(0, 23))

            order = {
                "order_id": f"{customer['customer_id']}-{order_id}",  # Unique order ID
                "customer_id": customer['customer_id'],
                "order_amount": order_amount,
                "order_timestamp": order_time
            }

            orders.append(order)

    return orders

# Initialize the Faker instance
fake = Faker('de_DE')

# Generate customer data
customer_data = generate_german_customer_data(fake, num_customers=100)

# Generate orders
order_data = generate_orders(fake, customer_data, num_orders_per_customer=10)



# Save customer data to CSV
with open('example_data/customer_data.csv', 'w', newline='') as csvfile:
    fieldnames = customer_data[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for customer in customer_data:
        writer.writerow(customer)

# Save order data to CSV
with open('example_data/order_data.csv', 'w', newline='') as csvfile:
    fieldnames = order_data[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for order in order_data:
        writer.writerow(order)