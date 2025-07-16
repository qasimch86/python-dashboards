import pandas as pd
import numpy as np
import random
from faker import Faker
from collections import Counter
import os
os.chdir("Task3")
# Set random seed for reproducibility
fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)

NUM_USERS = 150
LOCATIONS = ["USA", "Germany", "UK", "Mexico", "Sweden", "Austria", "Canada", "France"]
PRODUCTS = ["Product A", "Product B"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"]

# Generate customers with unique ID
users = []
for user_id in range(1, NUM_USERS + 1):
    country = random.choice(LOCATIONS)
    status = random.choices(["Active", "Inactive"], weights=[0.85, 0.15])[0]
    users.append({
        "UserID": user_id,
        "Name": fake.name(),
        "Email": fake.email(),
        "Location": country,
        "Status": status
    })

customer_df = pd.DataFrame(users)

# Generate orders for users (one-to-many)
orders = []
order_id = 1
for user_id in customer_df["UserID"]:
    # Each user can have 0 to 5 orders
    num_orders = random.choices([0, 1, 2, 3, 4, 5], weights=[0.1, 0.4, 0.2, 0.15, 0.1, 0.05])[0]
    for _ in range(num_orders):
        product = random.choice(PRODUCTS)
        month = random.choice(MONTHS)
        quantity = random.randint(1, 5)
        orders.append({
            "OrderID": order_id,
            "UserID": user_id,
            "Product": product,
            "Month": month,
            "Quantity": quantity
        })
        order_id += 1

orders_df = pd.DataFrame(orders)

# Now create summary data
registered_users = len(customer_df)
weekly_visitors = int(registered_users * np.random.uniform(0.5, 0.8))
subscriptions = len(customer_df[customer_df["Status"] == "Active"])

summary_data = {
    "Registered Users": registered_users,
    "Weekly Visitors": weekly_visitors,
    "Subscriptions": subscriptions,
    "Total Orders": len(orders_df)
}

# Location map data remains the same
location_counts = customer_df["Location"].value_counts().reset_index()
location_counts.columns = ["Country", "Users"]
map_df = location_counts.sort_values(by="Country")

# Monthly sales by product calculated from orders
sales_data = []
for month in MONTHS:
    month_orders = orders_df[orders_df["Month"] == month]
    product_a_sales = month_orders[month_orders["Product"] == "Product A"]["Quantity"].sum()
    product_b_sales = month_orders[month_orders["Product"] == "Product B"]["Quantity"].sum()
    sales_data.append({
        "Month": month,
        "Product A": product_a_sales,
        "Product B": product_b_sales
    })
sales_df = pd.DataFrame(sales_data)

# Gauge data: Sales Index per country based on orders by active users
active_users = customer_df[customer_df["Status"] == "Active"]["UserID"].tolist()
active_orders = orders_df[orders_df["UserID"].isin(active_users)]
active_counts = active_orders.merge(customer_df[['UserID', 'Location']], on='UserID')
country_order_counts = active_counts["Location"].value_counts()
gauge_df = pd.DataFrame([
    {"Country": c, "Sales Index": min(100, int((count / active_orders.shape[0]) * 100))}
    for c, count in country_order_counts.items()
])

# Save CSV files
output_dir = "."
customer_df.to_csv(os.path.join(output_dir, "fake_customer_details.csv"), index=False)
orders_df.to_csv(os.path.join(output_dir, "fake_orders.csv"), index=False)
map_df.to_csv(os.path.join(output_dir, "fake_map_data.csv"), index=False)
sales_df.to_csv(os.path.join(output_dir, "fake_monthly_sales.csv"), index=False)
gauge_df.to_csv(os.path.join(output_dir, "fake_sales_comparison.csv"), index=False)

# Print samples
print("📊 Summary:")
print(summary_data)

print("\n👤 Sample Customers:")
print(customer_df.head())

print("\n🛒 Sample Orders:")
print(orders_df.head())

print("\n🗺️ Map Data:")
print(map_df)

print("\n📈 Monthly Sales:")
print(sales_df)

print("\n🕹️ Gauge Data:")
print(gauge_df)
