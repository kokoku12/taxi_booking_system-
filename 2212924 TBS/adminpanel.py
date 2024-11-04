import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pymysql
from bokingpanel import open_booking_panel





def admin_panel():
    # Function to prompt the user for a booking ID to edit
    def ask_for_booking_id():
        booking_id = simpledialog.askinteger("Edit Booking", "Enter Booking ID to edit:")
        return booking_id if booking_id is not None else None
    

    

     # Function to view all bookings in a separate window
    def view_bookings():
        try:
             # Connect to the database and retrieve booking data
            with pymysql.connect(host='localhost', user='root', password='Neil12345.', database='customer_booking_data') as con:
                mycursor = con.cursor()
                query = 'SELECT * FROM customer_booking_data'
                mycursor.execute(query)
                data = mycursor.fetchall()

             # Create a new window for displaying booking data
            data_window = tk.Toplevel(root)
            data_window.title("Booking Data")

             # Create a canvas to display the data
            canvas = tk.Canvas(data_window)
            canvas.pack(expand=True, fill="both")
            
             # Define headers for the data
            headers = ("Booking ID", "Destination", "Destination Postcode", "Location", "Location Postcode", "Quantity", "Travel Type", "Time Hour", "Time Minute", "AM/PM", "Date","driver_id","accepted_by")
            # Display headers in the canvas
            for col, header in enumerate(headers):
                tk.Label(canvas, text=header, relief=tk.RIDGE, borderwidth=1, width=15).grid(row=0, column=col)

            # Display data in the canvas
            for row_idx, row_data in enumerate(data):
                for col_idx, cell_data in enumerate(row_data):
                    tk.Label(canvas, text=cell_data, relief=tk.RIDGE, borderwidth=1, width=15).grid(row=row_idx + 1, column=col_idx)

        except Exception as e:
            # Display an error message if data retrieval fails
            messagebox.showerror('Error', f'Error retrieving data: {str(e)}')

    def assign_booking():
         # Function to prompt the user for a booking ID to assign
        selected_booking_id = ask_for_booking_id()

         # Check if a booking ID was selected
        if selected_booking_id:
             # Create a new window for assigning the booking to a driver
            assign_window = tk.Toplevel(root)
            assign_window.title(f"Assign Booking {selected_booking_id} to Driver")

             # Display a label for the assign window
            tk.Label(assign_window, text=f"Assign Booking {selected_booking_id} to Driver", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

            # Add widgets for selecting a driver or entering driver details
            # For simplicity, I'll add an Entry for entering driver ID
            tk.Label(assign_window, text="Driver ID:").grid(row=1, column=0, pady=5, padx=5, sticky=tk.W)
            driver_id_entry = ttk.Entry(assign_window)
            driver_id_entry.grid(row=1, column=1, pady=5, padx=5, sticky=tk.W)

            # Button to assign the booking to a driver
            assign_button = ttk.Button(assign_window, text="Assign", command=lambda: assign_booking_to_driver(selected_booking_id, driver_id_entry.get(), assign_window))
            assign_button.grid(row=2, column=0, columnspan=2, pady=10)
    
    # Function to assign a booking to a driver
    def assign_booking_to_driver(booking_id, driver_id, assign_window):
        try:
            # Connect to the database and begin a transaction
            with pymysql.connect(host='localhost', user='root', password='Neil12345.', database='customer_booking_data') as con:
                mycursor = con.cursor()
                con.begin()

                # Add logic for assigning booking to driver here
                update_query = 'UPDATE customer_booking_data SET driver_id = %s WHERE Booking_id = %s'
                mycursor.execute(update_query, (driver_id, booking_id))

                # Commit the changes and display a success message
                con.commit()
                messagebox.showinfo('Success', f'Booking {booking_id} Assigned to Driver {driver_id}')

                # Close the assign window after successful assignment
                assign_window.destroy()

        except Exception as e:
            # Rollback the transaction and display an error message
            con.rollback()
            messagebox.showerror('Error', f'Error assigning booking to driver: {str(e)}')

    # Function to create a new booking
    def make_booking():
        open_booking_panel()

    # Function to update a booking
    def update_booking(booking_id, entry_values):
            try:
                # Connect to the database and begin a transaction
                with pymysql.connect(host='localhost', user='root', password='Neil12345.', database='customer_booking_data') as con:
                    mycursor = con.cursor()
                    con.begin()


                     # Update query to modify the booking data
                    update_query = 'UPDATE customer_booking_data SET destination = %s, destination_postcode = %s, location = %s, location_postcode = %s, quantity = %s, travel_type = %s, time_hour = %s, time_minute = %s, ampm = %s, date = %s WHERE Booking_id = %s'
                    mycursor.execute(update_query, (*[value.get() for value in entry_values], booking_id))


                    
            # Commit the changes and display a success message
                    con.commit()
                    messagebox.showinfo('Success', 'Booking Updated')

            # Rollback the transaction and display an error message
            except Exception as e:
                con.rollback()
                messagebox.showerror('Error', f'Error updating data: {str(e)}')

    
# Function to edit an existing booking
    def edit_booking_function():
        # Prompt the user for a booking ID to edit
        selected_booking_id = ask_for_booking_id()

        if selected_booking_id:
            try:
                con = pymysql.connect(host='localhost', user='root', password='Neil12345.', database='customer_booking_data')
                mycursor = con.cursor()

                # Fetch the existing data for the selected Booking ID
                query = 'SELECT * FROM customer_booking_data WHERE Booking_id = %s'
                mycursor.execute(query, (selected_booking_id,))
                existing_data = mycursor.fetchone()

                if existing_data:
                    # Create a new window for editing
                    edit_window = tk.Toplevel(root)
                    edit_window.title(f"Edit Booking {selected_booking_id}")

                    tk.Label(edit_window, text=f"Edit Booking {selected_booking_id}", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

                    # Labels and entry widgets for each field
                    labels = ["Destination:", "Post Code:", "Location:", "Post Code:", "Quantity:", "Travel Type:", "Time Hour:", "Time Minute:", "AM/PM:", "Date:"]
                    for i, label in enumerate(labels):
                        tk.Label(edit_window, text=label).grid(row=i + 1, column=0, pady=5, padx=5, sticky=tk.W)

                    entry_values = [tk.StringVar(value=value) for value in existing_data[1:]]
                    entries = [ttk.Entry(edit_window, textvariable=value) for value in entry_values]
                    for i, entry in enumerate(entries):
                        entry.grid(row=i + 1, column=1, pady=5, padx=5, sticky=tk.W)

                    # Update button
                    update_button = ttk.Button(edit_window, text="Update Booking", command=lambda: update_booking(selected_booking_id, entry_values))
                    update_button.grid(row=len(labels) + 1, column=0, columnspan=2, pady=10)

                else:
                    messagebox.showwarning('Warning', 'Booking ID not found')

            except Exception as e:
                messagebox.showerror('Error', f'Error editing booking: {str(e)}')
            finally:
                con.close()
                
        
    def cancel_booking():
         # Function to prompt the user for a booking ID to cancel
        selected_booking_id = ask_for_booking_id()

# Check if a booking ID was selected
        if selected_booking_id:
            try:
                # Connect to the database and fetch existing data for the selected Booking ID
                with pymysql.connect(host='localhost', user='root', password='Neil12345.', database='customer_booking_data') as con:
                    mycursor = con.cursor()
                    query = 'SELECT * FROM customer_booking_data WHERE Booking_id = %s'
                    mycursor.execute(query, (selected_booking_id,))
                    existing_data = mycursor.fetchone()

                     # Check if data for the selected Booking ID exists

                    if existing_data:
                        # Display a confirmation message with booking details
                        confirmation_message = f"Are you sure you want to cancel the booking with the following details?\n\n"
                        confirmation_message += f"Booking ID: {existing_data[0]}\n"
                        confirmation_message += f"Destination: {existing_data[1]}\n"
                        confirmation_message += f"Location: {existing_data[3]}\n"
                        confirmation_message += f"Quantity: {existing_data[5]}\n"
                        confirmation_message += f"Travel Type: {existing_data[6]}\n"
                        confirmation_message += f"Time: {existing_data[7]}:{existing_data[8]} {existing_data[9]}\n"
                        confirmation_message += f"Date: {existing_data[10]}\n\n"

                         # Ask for confirmation to cancel the booking
                        confirmed = messagebox.askyesno("Confirm Cancellation", confirmation_message)

                        if confirmed:
                            # Execute DELETE query to remove the booking from the database
                            delete_query = 'DELETE FROM customer_booking_data WHERE Booking_id = %s'
                            mycursor.execute(delete_query, (selected_booking_id,))
                            con.commit()
                            # Display success message if the booking is canceled

                            messagebox.showinfo('Success', 'Booking Canceled')
                        else:
                            # Display info message if the cancellation is canceled
                            messagebox.showinfo('Info', 'Booking Cancellation Cancelled')

                    else:
                        # Display a warning if the Booking ID is not found
                        messagebox.showwarning('Warning', 'Booking ID not found')

            except Exception as e:
                # Display an error message if canceling the booking fails
                messagebox.showerror('Error', f'Error canceling booking: {str(e)}')

    def monitor_data():
        try:
            # Connect to the MySQL server and fetch the list of databases
            with pymysql.connect(host='localhost', user='root', password='Neil12345.') as con:
                mycursor = con.cursor()
                query = "SHOW DATABASES"
                mycursor.execute(query)
                databases = mycursor.fetchall()


            # Create a new window to display the connected databases
            data_window = tk.Toplevel(root)
            data_window.title("Connected Databases")

            # Create a canvas to display the data
            canvas = tk.Canvas(data_window)
            canvas.pack(expand=True, fill="both")

            # Define headers for the data
            headers = ("Database",)
            for col, header in enumerate(headers):
                tk.Label(canvas, text=header, relief=tk.RIDGE, borderwidth=1, width=20).grid(row=0, column=col)

             # Display the list of connected databases
            for row_idx, row_data in enumerate(databases):
                tk.Label(canvas, text=row_data[0], relief=tk.RIDGE, borderwidth=1, width=20).grid(row=row_idx + 1, column=0)

        except Exception as e:
             # Display an error message if retrieving the database list fails
            messagebox.showerror('Error', f'Error retrieving database list: {str(e)}')

# Main part of the code...

# Creating the root window and setting up the button
    root = tk.Tk()
    root.title("Admin Dashboard")

    style = ttk.Style()
    style.configure('TButton', font=('Helvetica', 12), padding=10)

    view_bookings_button = ttk.Button(root, text="View Bookings", command=view_bookings)
    assign_booking_button = ttk.Button(root, text="Assign Booking to Driver", command=assign_booking)
    make_booking_button = ttk.Button(root, text="Make Booking for Customer", command=make_booking)
    edit_booking_button = ttk.Button(root, text="Edit Booking for Customer", command=edit_booking_function)
    cancel_booking_button = ttk.Button(root, text="Cancel Booking for Customer", command=cancel_booking)
    monitor_data_button = ttk.Button(root, text="Monitor System Data", command=monitor_data)

    # Grid layout for the buttons
    view_bookings_button.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
    assign_booking_button.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
    make_booking_button.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
    edit_booking_button.grid(row=1, column=1, padx=10, pady=10, sticky='ew')
    cancel_booking_button.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
    monitor_data_button.grid(row=2, column=1, padx=10, pady=10, sticky='ew')

    # Start the Tkinter event loop
    root.mainloop()