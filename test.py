import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os



# File paths for CSVs
PASSENGERS_CSV = 'passengers.csv'
FLIGHTS_CSV = 'flights.csv'


# Create CSV files if they don't exist
if not os.path.exists(PASSENGERS_CSV):
    with open(PASSENGERS_CSV, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'ID', 'Gender', 'BirthDate', 'Username', 'Password'])

if not os.path.exists(FLIGHTS_CSV):
    with open(FLIGHTS_CSV, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['From', 'To', 'Date', 'Airline', 'FlightType'])

# Function to handle registration
def register_user():
    name = name_entry.get()
    user_id = id_entry.get()
    gender = gender_var.get()
    birthdate = birthdate_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if not all([name, user_id, gender, birthdate, username, password]):
        messagebox.showwarning("Input Error", "Please fill all fields.")
        return

    # Check if username already exists
    with open(PASSENGERS_CSV, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            if row[4] == username:
                messagebox.showwarning("Registration Error", "Username already exists.")
                return

    # Write to CSV
    with open(PASSENGERS_CSV, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([name, user_id, gender, birthdate, username, password])

    messagebox.showinfo("Success", "Registration successful!")
    register_window.destroy()

# Function to handle login
def login():
    username = login_username_entry.get()
    password = login_password_entry.get()

    if username == "admin" and password == "admin":
        open_admin_dashboard()
        return

    with open(PASSENGERS_CSV, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[4] == username and row[5] == password:
                open_user_dashboard()
                return
        messagebox.showwarning("Login Error", "Invalid username or password.")

# Function to open registration window
def open_registration():
    global register_window, name_entry, id_entry, gender_var, birthdate_entry, username_entry, password_entry
    register_window = tk.Toplevel(root)
    register_window.title("Register")

    tk.Label(register_window, text="Name:").grid(row=0, column=0)
    name_entry = tk.Entry(register_window)
    name_entry.grid(row=0, column=1)

    tk.Label(register_window, text="ID:").grid(row=1, column=0)
    id_entry = tk.Entry(register_window)
    id_entry.grid(row=1, column=1)

    tk.Label(register_window, text="Gender:").grid(row=2, column=0)
    gender_var = tk.StringVar()
    gender_dropdown = ttk.Combobox(register_window, textvariable=gender_var, values=["Male", "Female"])
    gender_dropdown.grid(row=2, column=1)

    tk.Label(register_window, text="Birth Date (DD/MM/YYYY):").grid(row=3, column=0)
    birthdate_entry = tk.Entry(register_window)
    birthdate_entry.grid(row=3, column=1)

    tk.Label(register_window, text="Username:").grid(row=4, column=0)
    username_entry = tk.Entry(register_window)
    username_entry.grid(row=4, column=1)

    tk.Label(register_window, text="Password:").grid(row=5, column=0)
    password_entry = tk.Entry(register_window, show="*")
    password_entry.grid(row=5, column=1)

    tk.Button(register_window, text="Register", command=register_user).grid(row=6, columnspan=2)

# Function to open admin dashboard
def open_admin_dashboard():
    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Dashboard")

    def add_flight():
        from_city = from_var.get()
        to_city = to_var.get()
        date = flight_date_entry.get()
        airline = airline_var.get()
        flight_type = flight_type_var.get()

        if not all([from_city, to_city, date, airline, flight_type]):
            messagebox.showwarning("Input Error", "Please fill all fields.")
            return

        with open(FLIGHTS_CSV, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([from_city, to_city, date, airline, flight_type])
        messagebox.showinfo("Success", "Flight added successfully!")

    def view_passengers():
        view_window = tk.Toplevel(admin_window)
        view_window.title("Passenger List")

        with open(PASSENGERS_CSV, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                tk.Label(view_window, text=f"Name: {row[0]}, ID: {row[1]}, Gender: {row[2]}, BirthDate: {row[3]}").pack()

    def view_flights():
        flight_window = tk.Toplevel(admin_window)
        flight_window.title("Flight List")

        with open(FLIGHTS_CSV, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                tk.Label(flight_window, text=f"From: {row[0]}, To: {row[1]}, Date: {row[2]}, Airline: {row[3]}, Type: {row[4]}").pack()

    # Admin can add flights
    tk.Label(admin_window, text="From:").grid(row=0, column=0)
    from_var = tk.StringVar()
    from_dropdown = ttk.Combobox(admin_window, textvariable=from_var, values=["Hanoi", "Ho Chi Minh City", "Da Nang"])
    from_dropdown.grid(row=0, column=1)

    tk.Label(admin_window, text="To:").grid(row=1, column=0)
    to_var = tk.StringVar()
    to_dropdown = ttk.Combobox(admin_window, textvariable=to_var, values=["Hanoi", "Ho Chi Minh City", "Da Nang"])
    to_dropdown.grid(row=1, column=1)

    tk.Label(admin_window, text="Date (DD/MM/YYYY):").grid(row=2, column=0)
    flight_date_entry = tk.Entry(admin_window)
    flight_date_entry.grid(row=2, column=1)

    tk.Label(admin_window, text="Airline:").grid(row=3, column=0)
    airline_var = tk.StringVar()
    airline_dropdown = ttk.Combobox(admin_window, textvariable=airline_var, values=["Vietnam Airlines", "Vietjet", "Bamboo Airways"])
    airline_dropdown.grid(row=3, column=1)

    tk.Label(admin_window, text="Flight Type:").grid(row=4, column=0)
    flight_type_var = tk.StringVar()
    flight_type_dropdown = ttk.Combobox(admin_window, textvariable=flight_type_var, values=["One-way", "Round-trip"])
    flight_type_dropdown.grid(row=4, column=1)

    tk.Button(admin_window, text="Add Flight", command=add_flight).grid(row=5, columnspan=2)

    # New Buttons for viewing passengers and flights
    tk.Button(admin_window, text="View Passengers", command=view_passengers).grid(row=6, columnspan=2)
    tk.Button(admin_window, text="View Flights", command=view_flights).grid(row=7, columnspan=2)


# Function to open user dashboard
def open_user_dashboard():
    user_window = tk.Toplevel(root)
    user_window.title("User Dashboard")

    def search_flights():
        from_city = from_var.get()
        to_city = to_var.get()
        date = flight_date_entry.get()
        flight_type = flight_type_var.get()

        with open(FLIGHTS_CSV, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            found_flights = []
            for row in reader:
                if row[0] == from_city and row[1] == to_city and row[2] == date and row[4] == flight_type:
                    found_flights.append(row)

            if found_flights:
                for flight in found_flights:
                    flight_label = tk.Label(user_window, text=f"Flight from {flight[0]} to {flight[1]} on {flight[2]} via {flight[3]} [{flight[4]}]")
                    flight_label.pack()
                    tk.Button(user_window, text="Book", command=lambda: messagebox.showinfo("Success", "Flight booked successfully!")).pack()
            else:
                messagebox.showinfo("No Flights", "No matching flights found.")

    # User can search for flights
    tk.Label(user_window, text="From:").pack()
    from_var = tk.StringVar()
    from_dropdown = ttk.Combobox(user_window, textvariable=from_var, values=["Hanoi", "Ho Chi Minh City", "Da Nang"])
    from_dropdown.pack()

    tk.Label(user_window, text="To:").pack()
    to_var = tk.StringVar()
    to_dropdown = ttk.Combobox(user_window, textvariable=to_var, values=["Hanoi", "Ho Chi Minh City", "Da Nang"])
    to_dropdown.pack()

    tk.Label(user_window, text="Date (DD/MM/YYYY):").pack()
    flight_date_entry = tk.Entry(user_window)
    flight_date_entry.pack()

    tk.Label(user_window, text="Flight Type:").pack()
    flight_type_var = tk.StringVar()
    flight_type_dropdown = ttk.Combobox(user_window, textvariable=flight_type_var, values=["One-way", "Round-trip"])
    flight_type_dropdown.pack()

    tk.Button(user_window, text="Search Flights", command=search_flights).pack()

# Root window
root = tk.Tk()
root.title("Flight Booking System")

# Login interface
tk.Label(root, text="Username:").grid(row=0, column=0)
login_username_entry = tk.Entry(root)
login_username_entry.grid(row=0, column=1)

tk.Label(root, text="Password:").grid(row=1, column=0)
login_password_entry = tk.Entry(root, show="*")
login_password_entry.grid(row=1, column=1)

tk.Button(root, text="Login", command=login).grid(row=2, columnspan=2)
tk.Button(root, text="Register", command=open_registration).grid(row=3, columnspan=2)

root.mainloop()
