"""
ChurnShield - Sample Data Generator
Generates a realistic Indian e-commerce customer dataset for testing.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

INDIAN_NAMES = [
    "Anjali Sharma", "Ramesh Gupta", "Priya Mehta", "Suresh Patel",
    "Kavita Singh", "Rajesh Kumar", "Sunita Verma", "Amit Shah",
    "Pooja Joshi", "Vikram Rao", "Neha Agarwal", "Deepak Nair",
    "Ritu Bansal", "Sanjay Mishra", "Meena Pillai", "Arjun Reddy",
    "Divya Iyer", "Kiran Desai", "Manish Tiwari", "Rekha Pandey",
    "Vijay Bhatt", "Anita Chaudhary", "Rohit Saxena", "Seema Yadav",
    "Nikhil Bose", "Smita Naik", "Gaurav Jain", "Lakshmi Rajan",
    "Aakash Malhotra", "Sheetal More", "Pankaj Thakur", "Usha Ghosh",
    "Tarun Kapoor", "Geeta Shukla", "Harish Kulkarni", "Mamta Das",
    "Vinod Srivastava", "Pallavi Hegde", "Sachin Dubey", "Asha Nambiar",
    "Mohit Choudhury", "Vandana Tripathi", "Ajay Garg", "Radha Menon",
    "Kunal Bajaj", "Swati Dixit", "Rahul Khanna", "Leela Pillai",
    "Dinesh Chauhan", "Nandita Roy"
]

def generate_dataset(n_customers=200):
    today = datetime(2026, 5, 9)
    records = []

    for i, name in enumerate(INDIAN_NAMES * (n_customers // len(INDIAN_NAMES) + 1)):
        if i >= n_customers:
            break

        # Assign customer type: loyal, at-risk, churned
        customer_type = random.choices(
            ["loyal", "at_risk", "churned"],
            weights=[0.4, 0.3, 0.3]
        )[0]

        if customer_type == "loyal":
            days_since_last = random.randint(1, 20)
            num_orders = random.randint(8, 30)
            total_spend = random.uniform(3000, 20000)
        elif customer_type == "at_risk":
            days_since_last = random.randint(21, 45)
            num_orders = random.randint(3, 8)
            total_spend = random.uniform(800, 5000)
        else:  # churned
            days_since_last = random.randint(46, 180)
            num_orders = random.randint(1, 4)
            total_spend = random.uniform(200, 2000)

        last_order_date = today - timedelta(days=days_since_last)
        avg_order_value = total_spend / num_orders

        records.append({
            "customer_id": f"CUST{1000 + i}",
            "customer_name": name + (f" {i}" if i >= len(INDIAN_NAMES) else ""),
            "last_order_date": last_order_date.strftime("%Y-%m-%d"),
            "num_orders": num_orders,
            "total_spend": round(total_spend, 2),
            "avg_order_value": round(avg_order_value, 2),
            "days_since_last_order": days_since_last,
        })

    df = pd.DataFrame(records)
    df.to_csv("sample_customers.csv", index=False)
    print(f"✅ Generated {len(df)} customer records → sample_customers.csv")
    return df

if __name__ == "__main__":
    generate_dataset(200)
