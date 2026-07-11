from db_connection import get_connection

connection = get_connection()

cursor = connection.cursor()

cursor.execute("""
SELECT retailer_name, headquarters
FROM retailers;
""")

print("Retailers:\n")

for row in cursor.fetchall():
    print(row)

cursor.close()
connection.close()

print("\nConnection closed.")