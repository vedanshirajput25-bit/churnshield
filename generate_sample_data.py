"""
ChurnShield — Sample Dataset Generator
Generates a realistic Indian e-commerce customer dataset for demo purposes.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

INDIAN_NAMES = [
    "Anjali Sharma", "Ramesh Gupta", "Priya Mehta", "Suresh Patel",
    "Kavita Singh", "Arun Kumar", "Neha Joshi", "Vikram Rao",
    "Sunita Verma", "Rohit Malhotra", "Pooja Nair", "Amit Desai",
    "Rekha Pillai", "Deepak Tiwari", "Smita Kulkarni", "Rajesh Iyer",
    "Anita Bose", "Manoj Pandey", "Geeta Srivastava", "Sanjay Mishra",
    "Lalita Reddy", "Vijay Chauhan", "Meena Ghosh", "Prakash Jain",
    "Usha Patil", "Naresh Dubey", "Savita Saxena", "Hemant Shah",
    "Radha Nair", "Kishore Menon", "Sudha Rao", "Pankaj Agarwal",
    "Lata Bhatt", "Dinesh Kaur", "Sarla Yadav", "Mohan Tripathi",
    "Chanda Kapoor", "Rajan Bajaj", "Seema Thakur", "Girish Bhatia",
    "Madhuri Soni", "Ashok Wagh", "Pushpa Pawar", "Nitin More",
    "Leela Naik", "Ganesh Sawant", "Padma Shinde", "Sunil Patil",
    "Varsha Jadhav", "Harish Gaikwad",
]

def generate_dataset(n=200):
    today = datetime.today()
    rows = []

    for i in range(n):
        name = random.choice(INDIAN_NAMES) + f" {i+1}"
        customer_id = f"CUST{1000 + i}"

        # Simulate churn behaviour
        profile = random.choices(
            ["loyal", "at_risk", "churned"],
            weights=[0.45, 0.30, 0.25]
        )[0]

        if profile == "loyal":
            last_days_ago = random.randint(1, 20)
            num_orders = random.randint(8, 25)
            total_spend = round(random.uniform(3000, 15000), 2)
        elif profile == "at_risk":
            last_days_ago = random.randint(21, 45)
            num_orders = random.randint(3, 8)
            total_spend = round(random.uniform(1000, 5000), 2)
        else:  # churned
            last_days_ago = random.randint(46, 120)
            num_orders = random.randint(1, 4)
            total_spend = round(random.uniform(200, 2000), 2)

        last_order_date = (today - timedelta(days=last_days_ago)).strftime("%Y-%m-%d")
        avg_order_value = round(total_spend / num_orders, 2)
        complaints = random.randint(0, 2) if profile != "loyal" else 0

        rows.append({
            "customer_id": customer_id,
            "customer_name": name,
            "last_order_date": last_order_date,
            "num_orders": num_orders,
            "total_spend": total_spend,
            "avg_order_value": avg_order_value,
            "complaints": complaints,
        })

    df = pd.DataFrame(rows)
    df.to_csv("sample_customers.csv", index=False)
    print(f"✅ Generated {n} customer records → sample_customers.csv")
    return df

if __name__ == "__main__":
    generate_dataset()
