import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('email_org_counts.sqlite')
cur = conn.cursor()

# Drop the table if it exists
cur.execute('DROP TABLE IF EXISTS Counts')

# Create the table
cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')

# Prompt for the file name
file_name = input('Enter file name: ')
if len(file_name) < 1:
    file_name = 'mbox.txt'

# Open the file
try:
    file_handle = open(file_name)
except:
    print('File cannot be opened:', file_name)
    quit()

# Read each line in the file
for line in file_handle:
    if not line.startswith('From: '):
        continue
    pieces = line.split()
    email = pieces[1]
    # Extract the domain from the email address
    org = email.split('@')[1]
    # Check if the domain already exists in the database
    cur.execute('SELECT count FROM Counts WHERE org = ?', (org,))
    row = cur.fetchone()
    if row is None:
        cur.execute('INSERT INTO Counts (org, count) VALUES (?, 1)', (org,))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?', (org,))
    # Commit changes to the database
    conn.commit()

# SQL command to retrieve the data
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC'

# Print the results
print("Counts:")
for row in cur.execute(sqlstr):
    print(row[0], row[1])

# Close the cursor and the connection
cur.close()
