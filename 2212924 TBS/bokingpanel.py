import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import pymysql
from tkinter import messagebox
from tkinter import simpledialog


def open_booking_panel():

    def ask_for_booking_id():
        # Use a simple dialog to ask for the Booking ID
        booking_id = simpledialog.askinteger("Edit Booking", "Enter Booking ID to edit:")
        return booking_id
    
    def cancel_booking_function():
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
                    # Display existing data and confirmation message
                    confirmation_message = f"Are you sure you want to cancel the booking with the following details?\n\n"
                    confirmation_message += f"Booking ID: {existing_data[0]}\n"
                    confirmation_message += f"Destination: {existing_data[1]}\n"
                    confirmation_message += f"Location: {existing_data[3]}\n"
                    confirmation_message += f"Quantity: {existing_data[5]}\n"
                    confirmation_message += f"Travel Type: {existing_data[6]}\n"
                    confirmation_message += f"Time: {existing_data[7]}:{existing_data[8]} {existing_data[9]}\n"
                    confirmation_message += f"Date: {existing_data[10]}\n\n"

                    confirmed = messagebox.askyesno("Confirm Cancellation", confirmation_message)

                    if confirmed:
                        # If user confirms, delete the booking from the database
                        delete_query = 'DELETE FROM customer_booking_data WHERE Booking_id = %s'
                        mycursor.execute(delete_query, (selected_booking_id,))
                        con.commit()

                        messagebox.showinfo('Success', 'Booking Canceled')
                    else:
                        messagebox.showinfo('Info', 'Booking Cancellation Cancelled')

                else:
                    messagebox.showwarning('Warning', 'Booking ID not found')

            except Exception as e:
                messagebox.showerror('Error', f'Error canceling booking: {str(e)}')
            finally:
                con.close()


    def edit_booking_function():
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
                    edit_window = tk.Toplevel(booking_panel)
                    edit_window.title("Edit Booking")

                    # Display existing data
                    tk.Label(edit_window, text="Edit Booking Information", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

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
                messagebox.showerror('Error', f'Error updating data: {str(e)}')

    def update_booking(booking_id, entry_values):
        try:
            con = pymysql.connect(host='localhost', user='root', password='Neil12345.', database='customer_booking_data')
            mycursor = con.cursor()

            # Update the data in the database
            update_query = 'UPDATE customer_booking_data SET destination = %s, destination_postcode = %s, location = %s, location_postcode = %s, quantity = %s, travel_type = %s, time_hour = %s, time_minute = %s, ampm = %s, date = %s WHERE Booking_id = %s'
            mycursor.execute(update_query, tuple(value.get() for value in entry_values) + (booking_id,))

            con.commit()
            con.close()

            messagebox.showinfo('Success', 'Booking Updated')

        except Exception as e:
            messagebox.showerror('Error', f'Error updating data: {str(e)}')





    def show_booking_data():
        try:
            con = pymysql.connect(host='localhost', user='root', password='Neil12345.', database='customer_booking_data')
            mycursor = con.cursor()

            query = 'SELECT * FROM customer_booking_data'
            mycursor.execute(query)
            data = mycursor.fetchall()

            con.close()

            # Create a new window to display the data
            data_window = tk.Toplevel(booking_panel)
            data_window.title("Booking Data")

            # Create a Canvas widget
            canvas = tk.Canvas(data_window)
            canvas.pack(expand=True, fill="both")

            # Create headers
            headers = ("Booking ID", "Destination", "Destination Postcode", "Location", "Location Postcode", "Quantity", "Travel Type", "Time Hour", "Time Minute", "AM/PM", "Date")
            for col, header in enumerate(headers):
                tk.Label(canvas, text=header, relief=tk.RIDGE, borderwidth=1, width=15).grid(row=0, column=col)

            # Populate the Canvas with data
            for row_idx, row_data in enumerate(data):
                for col_idx, cell_data in enumerate(row_data):
                    tk.Label(canvas, text=cell_data, relief=tk.RIDGE, borderwidth=1, width=15).grid(row=row_idx + 1, column=col_idx)

        except Exception as e:
            messagebox.showerror('Error', f'Error retrieving data: {str(e)}')




    def connect_bookingInfo ():
        if (
            destination_entry.get() == ''
            or post_code_destination_entry.get() == ''
            or post_code_location_entry.get() ==''
            or location_entry.get() == ''
            or quantity_spinbox.get() == ''
            or travel_type_combobox.get() == ''
            or time_spinbox_hour.get() == ''
            or time_spinbox_minute.get() ==''
            or ampm_combobox.get() == ''
            or date_entry.get_date() == ''
        ):
            messagebox.showwarning ('Booking have been created!', "All field are required")

        else:
            try:
                con = pymysql.connect(host='localhost', user='root', password= 'Neil12345.')
                mycursor = con.cursor()

            except:
                messagebox.showerror('Error', 'Data connectivity issue, try again')
                return
            
            try:
                query = 'create database if not exists customer_booking_data'
                mycursor.execute(query)
                query = 'use customer_booking_data'
                mycursor.execute(query)
                query = 'create table if not exists customer_booking_data (Booking_id int auto_increment primary key not null, destination varchar(50), destination_postcode varchar(50), location varchar(50), location_postcode varchar(50), quantity varchar(50), travel_type varchar(50), time_hour varchar(50), time_minute varchar(50), ampm varchar(50), date varchar(50))'
                mycursor.execute(query)

            except:
                mycursor.execute('use customer_booking_data')

            query = 'insert into customer_booking_data (destination , destination_postcode , location , location_postcode , quantity , travel_type , time_hour , time_minute , ampm , date) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(
                query,
                (
                    destination_entry.get(),
                    post_code_destination_entry.get(),
                    location_entry.get(),
                    post_code_location_entry.get(),
                    quantity_spinbox.get(),
                    travel_type_combobox.get(),
                    time_spinbox_hour.get(),
                    time_spinbox_minute.get(),
                    ampm_combobox.get(),
                    date_entry.get_date(),
                ),
            )

            con.commit()
            con.close()

            messagebox.showinfo('Sucess', 'Booking Created')



    booking_panel = tk.Tk()
    booking_panel.title("Booking App")

    # Create a frame for the form
    form_frame = ttk.Frame(booking_panel, padding="10")
    form_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))


    # Entry boxes
    destination_label = ttk.Label(form_frame, text="Destination:")
    destination_label.grid(row=0, column=0, pady=5, sticky=tk.W)
    destination_entry = ttk.Entry(form_frame)
    destination_entry.grid(row=0, column=1, pady=5, padx=5, sticky=tk.W)

    post_code_destination_label = ttk.Label(form_frame, text="Post Code:")
    post_code_destination_label.grid(row=0, column=2, pady=5, padx=5, sticky=tk.W)
    post_code_destination_entry = ttk.Entry(form_frame)
    post_code_destination_entry.grid(row=0, column=3, pady=5, padx=10, sticky=tk.W)

    location_label = ttk.Label(form_frame, text="Location:")
    location_label.grid(row=1, column=0, pady=5, sticky=tk.W)
    location_entry = ttk.Entry(form_frame)
    location_entry.grid(row=1, column=1, pady=5, padx=5, sticky=tk.W)

    post_code_location_label = ttk.Label(form_frame, text="Post Code:")
    post_code_location_label.grid(row=1, column=2, pady=5, padx=5, sticky=tk.W)
    post_code_location_entry = ttk.Entry(form_frame)
    post_code_location_entry.grid(row=1, column=3, pady=5, padx=10, sticky=tk.W)

    quantity_label = ttk.Label(form_frame, text="Quantity:")
    quantity_label.grid(row=2, column=0, pady=5, sticky=tk.W)
    quantity_spinbox = ttk.Spinbox(form_frame, from_=0, to=4)
    quantity_spinbox.grid(row=2, column=1, pady=5, padx=5, sticky=tk.W)

    travel_type_label = ttk.Label(form_frame, text="Travel Type:")
    travel_type_label.grid(row=3, column=0, pady=5, sticky=tk.W)
    travel_type_var = tk.StringVar()
    travel_type_combobox = ttk.Combobox(form_frame, textvariable=travel_type_var, values=["One Way", "Return"])
    travel_type_combobox.grid(row=3, column=1, pady=5, padx=5, sticky=tk.W)

    time_label = ttk.Label(form_frame, text="Time:")
    time_label.grid(row=4, column=0, pady=5, sticky=tk.W)

    # Spinbox for time (hours)
    time_label_hour = ttk.Label(form_frame, text="Time (HH):")
    time_label_hour.grid(row=4, column=0, pady=5, sticky=tk.W)
    time_spinbox_hour = ttk.Spinbox(form_frame, from_=0, to=12, width=2)
    time_spinbox_hour.grid(row=4, column=1, pady=5, padx=5, sticky=tk.W)

    # Spinbox for time (minutes)
    time_label_minute = ttk.Label(form_frame, text="Time (MM):")
    time_label_minute.grid(row=4, column=2, pady=5, sticky=tk.W)
    time_spinbox_minute = ttk.Spinbox(form_frame, from_=0, to=59, width=2)
    time_spinbox_minute.grid(row=4, column=3, pady=5, padx=5, sticky=tk.W)

    # Combobox for AM/PM
    ampm_combobox = ttk.Combobox(form_frame, values=["AM", "PM"])
    ampm_combobox.grid(row=4, column=4, pady=5, padx=5, sticky=tk.W)
    ampm_combobox.set("AM")

    date_label = ttk.Label(form_frame, text="Date:")
    date_label.grid(row=5, column=0, pady=5, sticky=tk.W)
    date_entry = DateEntry(form_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
    date_entry.grid(row=5, column=1, pady=5, padx=5, sticky=tk.W)

    # Create a frame for the buttons
    button_frame = ttk.Frame(booking_panel, padding="10")
    button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Create Booking button
    create_booking_button = ttk.Button(button_frame, text="Create Booking", command=connect_bookingInfo)
    create_booking_button.grid(row=0, column=0, padx=5, pady=10)

    # Edit Booking button
    edit_booking_button = ttk.Button(button_frame, text="Edit Booking", command= edit_booking_function)
    edit_booking_button.grid(row=0, column=1, padx=5, pady=10)

    # Cancel Booking button
    cancel_booking_button = ttk.Button(button_frame, text="Cancel Booking", command= cancel_booking_function)
    cancel_booking_button.grid(row=0, column=2, padx=5, pady=10)

    # Show Booking Data button
    show_data_button = ttk.Button(button_frame, text="Show Booking Data", command=show_booking_data)
    show_data_button.grid(row=0, column=3, padx=5, pady=10)




    booking_panel.mainloop()
