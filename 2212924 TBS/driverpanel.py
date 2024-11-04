import tkinter as tk
from tkinter import ttk, messagebox
import pymysql

class DriverPanelApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Driver Panel")
        self.geometry("600x400")

        self.logged_in_driver_id = 1
        print(self.logged_in_driver_id)

        # Create a frame on the left for available bookings
        available_frame = ttk.Frame(self)
        available_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Create "Refresh" button to refresh available bookings
        refresh_button = ttk.Button(available_frame, text="Refresh", command=self.refresh_available_bookings)
        refresh_button.pack(side=tk.TOP, pady=10)

        # Create "Accept Booking" button to accept the selected booking
        accept_button = ttk.Button(available_frame, text="Accept Booking", command=self.accept_booking)
        accept_button.pack(side=tk.TOP, pady=10)

        # Create a Treeview widget for available bookings
        columns_available = ("Booking ID", "Destination", "Date", "Accepted Status")
        self.tree_available = ttk.Treeview(available_frame, columns=columns_available, show='headings')

        # Set column headings and set a reasonable width for each column
        column_widths_available = (80, 150, 120, 120) 

        for col, width in zip(columns_available, column_widths_available):
            self.tree_available.column(col, width=width)
            self.tree_available.heading(col, text=col)

        # Pack the Treeview widget
        self.tree_available.pack(expand=True, fill='both')

        # Populate available bookings
        self.refresh_available_bookings()

        # Create a frame for buttons on the right
        button_frame = ttk.Frame(self)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # Create "View Booking" button for all bookings
        view_booking_button = ttk.Button(button_frame, text="View All Bookings", command=self.display_all_bookings)
        view_booking_button.pack(side=tk.TOP, pady=10)

        # Create "My Profile" button
        my_profile_button = ttk.Button(button_frame, text="My Profile", command=self.my_profile)
        my_profile_button.pack(side=tk.TOP, pady=20)

    def refresh_available_bookings(self):
        try:
            con = pymysql.connect(host='localhost', user='root', password='Neil12345.', database='customer_booking_data')
            mycursor = con.cursor()

            # Fetch available bookings
            query_available = 'SELECT * FROM customer_booking_data WHERE driver_id IS NULL'
            mycursor.execute(query_available)
            data_available = mycursor.fetchall()

            # Close the database connection
            con.close()

            # Clear existing items in the Treeview
            for item in self.tree_available.get_children():
                self.tree_available.delete(item)

            # Insert data into the Treeview for available bookings
            for row in data_available:
                accepted_status = "Not Accepted"
                self.tree_available.insert("", "end", values=(row[0], row[1], row[2], accepted_status))

        except Exception as e:
            messagebox.showerror('Error', f'Data connectivity issue: {e}')

    def my_profile(self):
        try:
            con = pymysql.connect(host='localhost', user='root', password='Neil12345.', database='driverdata')
            mycursor = con.cursor()

            query = f'SELECT * FROM driverdata WHERE id = {self.logged_in_driver_id}'
            print(query)
            mycursor.execute(query)
            data = mycursor.fetchall()

            con.close()
            print(data)

            if data:
                profile_window = tk.Toplevel(self)
                profile_window.title("My Profile")

                columns = ("id", "First Name", "Last Name", "Title", "Age", "Address", "Email", "Phone Number",
                        "License Number", "Plate Number", "Username", "Password")
                tree = ttk.Treeview(profile_window, columns=columns, show='headings')

                column_widths = (80, 80, 150, 120, 100, 120, 80, 100, 80, 80, 60, 120) 

                for col, width in zip(columns, column_widths):
                    tree.column(col, width=width)
                    tree.heading(col, text=col)

                for row in data:
                    column_mapping = dict(zip(columns, row))
                    tree_values = [column_mapping[col] for col in columns]
                    tree.insert("", "end", values=tree_values)

                tree.pack(expand=True, fill='both')
            else:
                messagebox.showinfo('Info', 'No profile data found for the logged-in driver.')

        except Exception as e:
            print(f'Error: {e}')
            messagebox.showerror('Error', f'Data connectivity issue: {e}')

    def display_all_bookings(self):
        try:
            con = pymysql.connect(host='localhost', user='root', password='Neil12345.', database='customer_booking_data')
            mycursor = con.cursor()

            # Fetch data based on the provided query
            query = '''
                SELECT cbd.*, dd.id AS driver_id, dd.username AS driver_username
                FROM customer_booking_data cbd
                LEFT JOIN driverdata dd ON cbd.driver_id = dd.id
            '''
            mycursor.execute(query)
            data = mycursor.fetchall()

            # Close the database connection
            con.close()

            # Create a new window for displaying bookings
            bookings_window = tk.Toplevel(self)
            bookings_window.title("All Bookings")

            # Create a Treeview widget
            columns = ("Booking ID", "Destination", "Destination Postcode", "Location", "Location Postcode", "Quantity",
                    "Travel Type", "Time Hour", "Time Minute", "AM/PM", "Date", "Accepted Status", "Driver ID", "Driver Username")
            tree = ttk.Treeview(bookings_window, columns=columns, show='headings')

            # Set column headings and set a reasonable width for each column
            column_widths = (80, 150, 120, 100, 120, 80, 100, 80, 80, 60, 120, 120, 80, 120) 

            for col, width in zip(columns, column_widths):
                tree.column(col, width=width)
                tree.heading(col, text=col)

            # Insert data into the Treeview
            for row in data:
                accepted_status = "Accepted" if row[11] == self.logged_in_driver_id else "Not Accepted"
                print(row)
                driver_username = row[14] if row[11] is not None else "N/A"
                tree.insert("", "end", values=row[:11] + (accepted_status, row[13], driver_username))

            # Pack the Treeview widget
            tree.pack(expand=True, fill='both')

        except Exception as e:
            messagebox.showerror('Error', f'Data connectivity issue: {e}')
            
    def display_assigned_bookings(self):
        try:
            con = pymysql.connect(host='localhost', user='root', password='Neil12345.', database='customer_booking_data')
            mycursor = con.cursor()

            # Fetch data based on the provided query, joining customer_booking_data and driverdata tables
            query = '''
                SELECT cbd.*, dd.first_name, dd.last_name, dd.plate_number
                FROM customer_booking_data cbd
                JOIN driverdata dd ON cbd.driver_id = dd.id
                WHERE cbd.driver_id = %s
            '''
            mycursor.execute(query, (self.logged_in_driver_id,))
            data = mycursor.fetchall()

            # Close the database connection
            con.close()

            # Create a new window for displaying assigned bookings
            bookings_window = tk.Toplevel(self)
            bookings_window.title("Assigned Bookings")

            # Create a Treeview widget with additional columns for driver information
            columns = ("Booking ID", "Destination", "Destination Postcode", "Location", "Location Postcode", "Quantity",
                       "Travel Type", "Time Hour", "Time Minute", "AM/PM", "Date", "Driver ID", "Driver First Name",
                       "Driver Last Name", "Driver Plate Number")
            tree = ttk.Treeview(bookings_window, columns=columns, show='headings')

            # Set column headings and set a reasonable width for each column
            column_widths = (80, 150, 120, 100, 120, 80, 100, 80, 80, 60, 120, 80, 80, 80, 120)

            for col, width in zip(columns, column_widths):
                tree.column(col, width=width)
                tree.heading(col, text=col)

            # Insert data into the Treeview
            for row in data:
                tree.insert("", "end", values=row)

            # Pack the Treeview widget
            tree.pack(expand=True, fill='both')

        except Exception as e:
            messagebox.showerror('Error', f'Data connectivity issue: {e}')

    def accept_booking(self):
        # Get the selected item in the Treeview
        selected_item = self.tree_available.selection()

        if not selected_item:
            messagebox.showinfo('Info', 'Please select a booking to accept.')
            return

        # Get the data of the selected item
        booking_data = self.tree_available.item(selected_item, 'values')

        if not booking_data:
            messagebox.showinfo('Info', 'No booking data available for the selected item.')
            return

        try:
            con = pymysql.connect(host='localhost', user='root', password='Neil12345.', database='customer_booking_data', autocommit=False)
            mycursor = con.cursor()

            # Update the booking with the driver_id and accepted_by
            query_update = 'UPDATE customer_booking_data SET driver_id = %s, accepted_by = %s WHERE booking_id = %s'
            mycursor.execute(query_update, (self.logged_in_driver_id, self.logged_in_driver_id, booking_data[0]))

            # Commit the transaction
            con.commit()

            # Update the Treeview with accepted status
            accepted_status = "Accepted"
            self.tree_available.item(selected_item, values=(booking_data[0], booking_data[1], booking_data[2], accepted_status))

        except Exception as e:
            # Rollback the transaction in case of an error
            con.rollback()
            messagebox.showerror('Error', f'Data connectivity issue: {e}')

        finally:
            # Close the database connection
            con.close()

if __name__ == "__main__":
    app = DriverPanelApp()
    app.mainloop()
