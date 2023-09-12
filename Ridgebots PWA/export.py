import sqlite3
import csv

# Connect to the SQLite database
sqlite_conn = sqlite3.connect('finance.db')
cursor = sqlite_conn.cursor()

# Define a list of table names to export
table_names = ['users', 'roster', 'parts', 'calendar', 'records', 'admin', 'team_todo', 'personal_todo']

for table_name in table_names:
    # Execute a query to select data from the current table
    cursor.execute(f"SELECT * FROM {table_name}")
    
    # Fetch all rows from the query result
    rows = cursor.fetchall()
    
    # Define a CSV file name for export (e.g., users.csv, roster.csv, etc.)
    csv_filename = f'{table_name}.csv'
    
    # Write the data to a CSV file
    with open(csv_filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # Write the header row
        header = [description[0] for description in cursor.description]
        csv_writer.writerow(header)
        
        # Write the data rows
        csv_writer.writerows(rows)

# Close the SQLite connection
sqlite_conn.close()
