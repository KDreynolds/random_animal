import sqlite3
import json

try:
    conn = sqlite3.connect('animals.db')
    cursor = conn.cursor()
    print("Connected to SQLite.")

    # Create table
    cursor.execute('''CREATE TABLE IF NOT EXISTS animals
                      (name TEXT, image TEXT)''')
    print("Table 'animals' is ready.")

    with open('animal_data.json', 'r') as file:
        data = json.load(file)
        print(f"Loaded data from animal_data.json with {len(data)} records.")

        for entry in data:
            name = entry.get('name')
            image = entry.get('image')
            if name and image:  # Ensuring that both name and image are present
                cursor.execute("INSERT INTO animals (name, image) VALUES (?, ?)", (name, image))
            else:
                print(f"Skipping entry due to missing data: {entry}")

    conn.commit()
    print("Data inserted into 'animals' table.")

except sqlite3.Error as e:
    print(f"SQLite error: {e}")
finally:
    conn.close()
    print("SQLite connection is closed.")
