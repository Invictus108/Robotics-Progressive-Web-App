import psycopg2
import csv

# PostgreSQL database URL (replace with your Heroku PostgreSQL URL)
postgresql_url = 'postgres://nafokqkmphelnu:f4f0cb19926abce6047900e9fcc3a753d0b93e3babb7604e4dcb91303e3c3fb4@ec2-3-210-173-88.compute-1.amazonaws.com:5432/daic9qmio2t2df'


# List of CSV files to import (corresponding to the tables)
csv_files = ['users.csv', 'roster.csv', 'parts.csv', 'calendar.csv', 'records.csv', 'admin.csv', 'team_todo.csv', 'personal_todo.csv']

# Connect to PostgreSQL database
conn = psycopg2.connect(postgresql_url)
cursor = conn.cursor()

for csv_filename in csv_files:
    # Extract the table name from the CSV filename (e.g., "users.csv" -> "users")
    table_name = csv_filename.split('.')[0]

    # Open and read the CSV file
    with open(csv_filename, 'r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)

        # Skip the header row
        next(csv_reader)

        # Get the header row to determine column names
        header_row = next(csv_reader)

        # Construct the INSERT SQL query dynamically based on the table structure
        columns = ', '.join(header_row)
        placeholders = ', '.join(['%s'] * len(header_row))
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        # Insert each row into the PostgreSQL table
        for row in csv_reader:
            cursor.execute(insert_query, row)  # Pass the data row directly

# Commit the changes and close the connection
conn.commit()
conn.close()

