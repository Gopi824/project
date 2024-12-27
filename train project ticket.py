
import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

# Initialize the database connection
conn = sqlite3.connect('train_booking.db')
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS trains (
    train_id INTEGER PRIMARY KEY,
    train_name TEXT NOT NULL,
    departure TEXT NOT NULL,
    destination TEXT NOT NULL,
    departure_time TEXT NOT NULL,
    seats_available INTEGER NOT NULL
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS bookings (
    booking_id INTEGER PRIMARY KEY,
    train_id INTEGER NOT NULL,
    passenger_name TEXT NOT NULL,
    passenger_age INTEGER NOT NULL,
    booking_time TEXT NOT NULL,
    FOREIGN KEY (train_id) REFERENCES trains (train_id)
)
''')
conn.commit()

# Initialize tkinter window
root = tk.Tk()
root.title("Train Booking System")

# Initialize trains (Sample Data)
def initialize_trains():
    trains = [
        (1, "Express A", "City A", "City B", "2024-11-15 10:00:00", 50),
        (2, "Express B", "City A", "City C", "2024-11-15 12:00:00", 50),
        (3, "Express C", "City B", "City D", "2024-11-15 14:00:00", 50),
    ]
    cursor.executemany('INSERT OR IGNORE INTO trains VALUES (?, ?, ?, ?, ?, ?)', trains)
    conn.commit()

initialize_trains()

# View available trains
def view_trains():
    cursor.execute("SELECT * FROM trains WHERE seats_available > 0")
    trains = cursor.fetchall()
    train_info = "\n".join(
        [f"ID: {train[0]}, Name: {train[1]}, From: {train[2]}, To: {train[3]}, "
         f"Departure: {train[4]}, Seats: {train[5]}" for train in trains]
    )
    messagebox.showinfo("Available Trains", train_info)

# Book a ticket
def book_ticket():
    train_id = int(train_id_entry.get())
    passenger_name = name_entry.get()
    passenger_age = int(age_entry.get())
    
    cursor.execute("SELECT seats_available FROM trains WHERE train_id = ?", (train_id,))
    result = cursor.fetchone()
    
    if result and result[0] > 0:
        cursor.execute("UPDATE trains SET seats_available = seats_available - 1 WHERE train_id = ?", (train_id,))
        booking_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO bookings (train_id, passenger_name, passenger_age, booking_time) "
                       "VALUES (?, ?, ?, ?)", (train_id, passenger_name, passenger_age, booking_time))
        conn.commit()
        messagebox.showinfo("Booking Success", f"Ticket booked for {passenger_name} on Train ID {train_id}.")
    else:
        messagebox.showerror("Error", "No seats available on this train.")

# View all bookings
def view_bookings():
    cursor.execute('''
    SELECT b.booking_id, t.train_name, b.passenger_name, b.passenger_age, b.booking_time
    FROM bookings b
    JOIN trains t ON b.train_id = t.train_id
    ''')
    bookings = cursor.fetchall()
    booking_info = "\n".join(
        [f"Booking ID: {booking[0]}, Train: {booking[1]}, Passenger: {booking[2]}, Age: {booking[3]}, "
         f"Time: {booking[4]}" for booking in bookings]
    )
    messagebox.showinfo("All Bookings", booking_info)

# Delete a booking
def delete_booking():
    booking_id = int(booking_id_entry.get())
    cursor.execute("DELETE FROM bookings WHERE booking_id = ?", (booking_id,))
    conn.commit()
    messagebox.showinfo("Delete Success", f"Booking ID {booking_id} has been deleted.")

# Layout the tkinter window
tk.Label(root, text="Train ID:").grid(row=0, column=0)
train_id_entry = tk.Entry(root)
train_id_entry.grid(row=0, column=1)

tk.Label(root, text="Passenger Name:").grid(row=1, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=1, column=1)

tk.Label(root, text="Passenger Age:").grid(row=2, column=0)
age_entry = tk.Entry(root)
age_entry.grid(row=2, column=1)

tk.Button(root, text="View Trains", command=view_trains).grid(row=3, column=0)
tk.Button(root, text="Book Ticket", command=book_ticket).grid(row=3, column=1)
tk.Button(root, text="View Bookings", command=view_bookings).grid(row=4, column=0)

tk.Label(root, text="Booking ID:").grid(row=5, column=0)
booking_id_entry = tk.Entry(root)
booking_id_entry.grid(row=5, column=1)
tk.Button(root, text="Delete Booking", command=delete_booking).grid(row=6, column=0)

root.mainloop()

# Close database connection on exit
conn.close()
