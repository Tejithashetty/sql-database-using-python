import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",        # Change this if your DB is remote
    user="root",    # Replace with your MySQL username
    password="12345",# Replace with your MySQL password
    database="sales_db"      # Make sure this database exists
)

cursor = conn.cursor()

# Step 2: Create the 'sales' table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product VARCHAR(255),
    quantity INT,
    price DECIMAL(10,2)
)
''')

# Step 3: Optional - Insert sample data (you can comment this out after first run)
sample_data = [
    ('Apple', 15, 1500),
    ('Banana', 15, 700),
    ('Orange', 9, 1700),
    ('kiwi', 20, 3000),
    ('pears', 10, 1600),
    ('Orange', 28, 6000)
]

cursor.executemany('INSERT INTO sales (product, quantity, price) VALUES (%s, %s, %s)', sample_data)
conn.commit()

# Step 4: Query total quantity sold and total revenue by product and quantity bye price
query = '''
SELECT product, 
       SUM(quantity) AS total_qty, 
       ROUND(SUM(quantity * price), 2) AS revenue
FROM sales
GROUP BY product
'''

df = pd.read_sql(query, conn)

query2 = '''
SELECT product, price, SUM(quantity) AS total_qty
FROM sales
GROUP BY product, price
ORDER BY product, price
'''
df2 = pd.read_sql(query2, conn)


# Step 5: Print summary
print("Sales Summary:")
print(df)

print("\nQuantity by Product and Price:")
print(df2)

# Step 6: Plot revenue bar chart and quantity by price scatter plot
df.plot(kind='bar', x='product', y='revenue', color='green', legend=False)
plt.title("Revenue by Product")
plt.ylabel("Revenue ($)")
plt.xlabel("Product")
plt.tight_layout()
plt.savefig("sales_chart_mysql.png")
plt.show()# Save chart as PNG 

plt.clf()

pivot_df = df2.pivot(index='price', columns='product', values='total_qty').fillna(0)
pivot_df.plot(kind='bar', figsize=(8,6))
plt.title("Quantity by Price per Product")
plt.ylabel("Quantity Sold")
plt.xlabel("Price ($)")
plt.legend(title="Product")
plt.tight_layout()
plt.savefig("quantity_by_price.png")
plt.show()


# Step 7: Close the connection
cursor.close()
conn.close()
