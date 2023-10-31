import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime, timedelta
from collections import defaultdict
from faker import Faker

# Check if the directory "synthetic_ecommerce_data" exists. If not, create it.
if not os.path.exists('synthetic_ecommerce_data'):
    os.makedirs('synthetic_ecommerce_data')
if not os.path.exists('map_data'):
    sys.exit('The directory "map_data" does not exist. Please create it and try again.')

# Check if the file "uscities.csv" exists in the "map_data" directory. If not, exit the script.
if not os.path.isfile('map_data/uscities.csv'):
    sys.exit('The file "uscities.csv" does not exist in the "map_data" directory. Please add it and try again.')

fake = Faker()

# Define the number of orders, products, years, categories, and customers
num_years = 3
num_orders = 100
num_customers = 30
num_products = 10
categories = ['Electronics','Apparel', 'Home & Kitchen', 'Books']

high_return_categories = ['Electronics']
high_return_months = [12, 1]  
high_order_months_apparel = [8, 11, 12]
high_order_months_electronics = [8, 12]
return_rate = 0.15  # Default return rate

product_ids = [f'P{i+1:05d}' for i in range(num_products)]

def generate_product_name(category, index):
    electronics_adjectives = ['Super', 'Ultra', 'Extreme', 'Ultimate', 'Premium', 'Deluxe', 'Pro', 'Advanced', 'High-Performance', 'Elite']
    apparel_adjectives = ['Stylish', 'Comfortable', 'Chic', 'Trendy', 'Casual', 'Formal', 'Sophisticated', 'Elegant', 'Cool', 'Classy']
    home_kitchen_adjectives = ['Durable', 'Reliable', 'Efficient', 'Economical', 'Practical', 'Compact', 'Versatile', 'High-Quality', 'Modern', 'Classic']
    books_adjectives = ['Thrilling', 'Informative', 'Captivating', 'Inspiring', 'Provocative', 'Funny', 'Insightful', 'Exciting', 'Moving', 'Imaginative']
    
    electronics_brands = ['CoolTech', 'DigiTrend', 'TechAdvance', 'ElectroMatic', 'GigaGadget'] 
    apparel_brands = ['FashionFirst', 'StyleSquare', 'TrendTribe', 'EleganceEdge', 'ChicCharm'] 
    home_kitchen_brands = ['HomeEco', 'DomestiKing', 'HomeMate', 'KitchenCraft', 'ComfyCasa'] 
    books_brands = ['BookWorm', 'StorySphere', 'LiteraryLuxe', 'PagePremier', 'NovelNiche'] 

    electronics = ['Smartphone', 'Laptop', 'Headphone', 'Camera', 'Speaker']
    apparel = ['Shirt', 'Jeans', 'Jacket', 'Sneaker', 'Dress']
    home_kitchen = ['Mixer', 'Fridge', 'Oven', 'Toaster', 'Chair']
    books = ['Mystery Novel', 'Science Book', 'Fantasy Novel', 'History Book', 'Biography']

    if category == 'Electronics':
        product_type = np.random.choice(electronics)
        brand_name = np.random.choice(electronics_brands)
        adjective = np.random.choice(electronics_adjectives)
    elif category == 'Apparel':
        product_type = np.random.choice(apparel)
        brand_name = np.random.choice(apparel_brands)
        adjective = np.random.choice(apparel_adjectives)
    elif category == 'Home & Kitchen':
        product_type = np.random.choice(home_kitchen)
        brand_name = np.random.choice(home_kitchen_brands)
        adjective = np.random.choice(home_kitchen_adjectives)
    else:
        product_type = np.random.choice(books)
        brand_name = np.random.choice(books_brands)
        adjective = np.random.choice(books_adjectives)

    product_name = f'{brand_name} {adjective} {product_type} Series {index+1:05}'
    return product_name

def generate_product_price(category, product_name):
    product_type = product_name.split()[-3]  # Product type is the third word from the end in the product name

    if category == 'Electronics':
        if product_type == 'Smartphone':
            price = np.random.uniform(200, 1000)
        elif product_type == 'Laptop':
            price = np.random.uniform(500, 2000)
        elif product_type == 'Headphone':
            price = np.random.uniform(50, 300)
        elif product_type == 'Camera':
            price = np.random.uniform(300, 1500)
        else:  # Speaker
            price = np.random.uniform(100, 500)
            
    elif category == 'Apparel':
        if product_type == 'Shirt':
            price = np.random.uniform(20, 80)
        elif product_type == 'Jeans':
            price = np.random.uniform(30, 100)
        elif product_type == 'Jacket':
            price = np.random.uniform(50, 200)
        elif product_type == 'Sneaker':
            price = np.random.uniform(50, 200)
        else:  # Dress
            price = np.random.uniform(30, 150)
            
    elif category == 'Home & Kitchen':
        if product_type == 'Mixer':
            price = np.random.uniform(50, 200)
        elif product_type == 'Fridge':
            price = np.random.uniform(500, 2000)
        elif product_type == 'Oven':
            price = np.random.uniform(300, 1000)
        elif product_type == 'Toaster':
            price = np.random.uniform(20, 100)
        else:  # Chair
            price = np.random.uniform(50, 300)

    else:  # Books
        price = np.random.uniform(10, 30)

    return round(price, 2)

def get_random_zip(zip_string):
    # Split zips into a list
    zip_list = zip_string.split()

    # Pick a random zip to return
    return str(np.random.choice(zip_list)).zfill(5)

# Define customer preferences 
customer_prefs = {f'C{i+1:05}': np.random.choice(categories) for i in range(num_customers)}

# Define product demand
product_demand = {f'P{i+1:05}': np.random.randint(1, 5) for i in range(num_products)}

# Generate product data
product_categories = np.random.choice(categories, num_products)
product_names = [generate_product_name(category, i) for i, category in enumerate(product_categories)]
products = pd.DataFrame({
    'Product_ID': [f'P{i+1:05}' for i in range(num_products)],
    'Product_Name': product_names,
    'Category': product_categories,
    'Unit_Price': [generate_product_price(category, product_name) for category, product_name in zip(product_categories, product_names)]
})

# Load city-state pairs from CSV
city_data = pd.read_csv('map_data/uscities.csv')

# Convert 'zips' column to strings
city_data['zips'] = city_data['zips'].astype(str)

# Extract the first ZIP code from the ZIP code string
city_data['zip'] = city_data['zips'].apply(get_random_zip)

# Create list of tuples from DataFrame
city_state_zip = list(zip(city_data['city'], city_data['state_id'], city_data['zip']))

# Select random city-state-zip for each customer
locations = np.random.choice(len(city_state_zip), num_customers)
cities = [city_state_zip[i][0] for i in locations]
states = [city_state_zip[i][1] for i in locations]
zips = [city_state_zip[i][2] for i in locations]

# Gender Segmentation
customer_gender = ['Male', 'Female', 'Intersex', 'Indeterminate', 'Transsexual']  

# Birthyear Distribution Parameters
mean_birthyear = 1990
std_dev_birthyear = 10
min_birthyear = 1925
max_birthyear = 2005

# Generate Customer Birthyears
birthyears = np.random.normal(loc=mean_birthyear, scale=std_dev_birthyear, size=num_customers)
birthyears = np.round(birthyears)  # round to nearest integer
birthyears = np.clip(birthyears, min_birthyear, max_birthyear)  # clip to min_birthyear and max_birthyear

# Generate Birthdates
birthdates = []
for year in birthyears:
    # Generate a random day in the year
    random_day = datetime(int(year), 1, 1) + timedelta(days=np.random.randint(365))
    birthdates.append(random_day.strftime('%Y-%m-%d'))  # store birthdate as string

# Generate customer data
customers = pd.DataFrame({
    'Customer_ID': [f'C{i+1:05}' for i in range(num_customers)],
    'Customer_Name': [fake.name() for i in range(num_customers)],
    'City': cities,
    'State': states,
    'ZIP': zips,
    'Country': ['USA' for i in range(num_customers)],
    'Gender': np.random.choice(customer_gender, num_customers, p=[0.48, 0.44, 0.04, 0.03, 0.01]),
    'Birthdate': birthdates
})

# Generate records 
orders = []
shippings = []
payments = []
product_reviews = []
inventory = []
returns = []

for i in range(num_orders):
    # Choose a random customer and product
    cust_id = f'C{np.random.randint(1, num_customers+1):05d}'
    prod_id = f'P{i%num_products+1:05d}'


    # Choose a random day
    day = datetime(2019, 1, 1) + timedelta(days=np.random.randint(0, 365 * num_years))

    # Adjust for seasonal trends
    if customer_prefs[cust_id] == 'Electronics' and day.month in high_order_months_electronics:
        num_items = np.random.poisson(5)
    elif customer_prefs[cust_id] == 'Apparel' and day.month in high_order_months_apparel:
        num_items = np.random.poisson(5)
    elif customer_prefs[cust_id] == 'Home & Kitchen' and day.month == 7:
        num_items = np.random.poisson(5)
    else:
        num_items = np.random.poisson(2)

    # Adjust for product demand
    num_items *= product_demand[prod_id]

    order_id = f'ORD{str(i+1).zfill(5)}'

    # Randomly select 1-5 products for this order
    order_product_ids = np.random.choice(product_ids, np.random.randint(1, 6))

    # Generate order data
    for prod_id in order_product_ids:
        # Append record to orders
        num_orders_today = np.random.randint(1, 11)
        orders.append({
            'Order_ID': order_id,
            'Product_ID': prod_id,
            'Quantity': num_orders_today,
            'Order_Date': day.strftime('%Y-%m-%d'),
            "Customer_ID": cust_id
        })
    # Append record to shippings
    shippings.append({
        'Order_ID': order_id,
        'Shipping_Method': np.random.choice(['Standard', 'Express']),
        'Shipping_Cost': np.round(np.random.uniform(5, 50), 2),
        'Estimated_Delivery_Date': (day + timedelta(days=np.random.randint(3, 7))).strftime('%Y-%m-%d'),
        'Actual_Delivery_Date': (day + timedelta(days=np.random.randint(3, 10))).strftime('%Y-%m-%d')
    })

    # Append record to payments
    payments.append({
        'Order_ID': order_id,
        'Payment_Method': np.random.choice(['Credit Card', 'PayPal', 'ApplePay']),
        'Payment_Status': np.random.choice(['Completed', 'Pending', 'Failed'], p=[0.9, 0.08, 0.02]),
        'Payment_Date': (day + timedelta(days=np.random.randint(0, 3))).strftime('%Y-%m-%d')
    })

    return_rate = 0.15

    # Convert products to a dataframe
    if not isinstance(products, pd.DataFrame):
        products = pd.DataFrame(products)

    # Check if order contains high return products
    if any(category in high_return_categories for category in products[products['Product_ID'].isin(order_product_ids)]['Category']):
        return_rate = 0.17  # Increase return rate

    # Check if order is made in high return months
    if day.month in high_return_months:
        return_rate = max(return_rate, 0.20)  # Increase return rate to 20%, if not already higher


    if np.random.rand() < return_rate: 
        # Randomly select a product from the order for return
        prod_id_returned = np.random.choice(order_product_ids)
        quantity_returned = np.random.randint(1, num_items+1) if num_items > 0 else 0

        returns.append({
            'Order_ID': order_id,
            'Product_ID': prod_id,
            'Quantity': quantity_returned,
            'Return_Date': (day + timedelta(days=np.random.randint(1,30))).strftime('%Y-%m-%d'),
            'Reason': np.random.choice(['Unsatisfied with product', 'Wrong product delivered', 'Product damaged', 'Product not needed']),
        })


    # Append record to product_reviews
    if np.random.rand() < 0.53: # 53% of orders will have a review
        product_reviews.append({
            'Order_ID': order_id,
            'Product_ID': prod_id,
            'Customer_ID': cust_id,
            'Review_Text': fake.sentence(),
            'Rating': np.random.randint(1, 6),
            'Review_Date': (day + timedelta(days=np.random.randint(7,30))).strftime('%Y-%m-%d')
        })
    
    # Append record to inventory
    inventory.append({
        'Product_ID': prod_id,
        'Quantity_In_Stock': np.random.randint(0,100),
        'Reorder_Level': np.random.randint(10, 20),
        'Reorder_Quantity': np.random.randint(20, 50)
    })


# Create orders, shippings, payments, product_reviews, and inventory dataframes
orders = pd.DataFrame(orders)
orders['Discount'] = (np.random.rand(len(orders))*0.5).round(2)  # New discount field in orders
shippings = pd.DataFrame(shippings)
payments = pd.DataFrame(payments)
product_reviews = pd.DataFrame(product_reviews)
inventory = pd.DataFrame(inventory)
returns = pd.DataFrame(returns)

# Merge orders and products to compute sales
sales_df = pd.merge(orders, products, how='inner', on='Product_ID')

# Compute sales for each record
sales_df['Sales'] = sales_df['Quantity'] * sales_df['Unit_Price']

# Convert 'Order_Date' to datetime and get year
sales_df['Order_Date'] = pd.to_datetime(sales_df['Order_Date'])
sales_df['Year'] = sales_df['Order_Date'].dt.year

# Get total sales per month and category
sales_df['Month'] = sales_df['Order_Date'].dt.month
sales_per_month_category = sales_df.groupby(['Year', 'Month', 'Category'])['Sales'].sum().reset_index()

# Initialize a list to store sales targets
sales_targets = []

for i in range(num_years):
    for month in range(1, 13):  # 12 months in a year
        for category in categories:
            # For the first year, set target as sales * 1.1
            if i == 0:
                last_month_sales = sales_per_month_category.loc[(sales_per_month_category['Year'] == 2019) 
                                                                 & (sales_per_month_category['Month'] == month)
                                                                 & (sales_per_month_category['Category'] == category), 'Sales'].values
                if last_month_sales.size > 0:
                    target = last_month_sales[0] * 1.1
                else:
                    target = 0
            else:
                # For subsequent years, set target as last year's sales * 1.1
                # Same target growth for each month
                last_year_sales = sales_per_month_category.loc[(sales_per_month_category['Year'] == 2019 + i - 1) 
                                                               & (sales_per_month_category['Month'] == month)
                                                               & (sales_per_month_category['Category'] == category), 'Sales'].values
                if last_year_sales.size > 0:
                    target = last_year_sales[0] * 1.1
                else:
                    target = 0

            sales_targets.append({
                'Year': 2019 + i,
                'Month': month,
                'Category': category,
                'Sales_Target': round(target, 2)
            })

# Convert sales_targets to a dataframe and save to CSV
sales_targets = pd.DataFrame(sales_targets)
sales_targets.to_csv('synthetic_ecommerce_data/sales_targets.csv', index=False)

# Export the other dataframes to CSV files!
orders.to_csv('synthetic_ecommerce_data/orders.csv', index=False)
products.to_csv('synthetic_ecommerce_data/products.csv', index=False)
customers.to_csv('synthetic_ecommerce_data/customers.csv', index=False)
shippings.to_csv('synthetic_ecommerce_data/shippings.csv', index=False)
payments.to_csv('synthetic_ecommerce_data/payments.csv', index=False)
product_reviews.to_csv('synthetic_ecommerce_data/product_reviews.csv', index=False)
inventory.to_csv('synthetic_ecommerce_data/inventory.csv', index=False)
returns.to_csv('synthetic_ecommerce_data/returns.csv', index=False)