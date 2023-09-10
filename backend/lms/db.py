import mysql.connector

# MySQL server configuration
host = "localhost"  # Replace with your MySQL server host
user = "root"  # Replace with your MySQL username
password = "Akhil@2002"  # Replace with your MySQL password

# Connect to MySQL server
try:
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
    )

    cursor = connection.cursor()

    # Database name
    database_name = "library"  # Replace with your desired database name

    # Create a new database
    cursor.execute(f"CREATE DATABASE {database_name}")

    print(f"Database '{database_name}' created successfully.")

except mysql.connector.Error as error:
    print(f"Error: {error}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed.")