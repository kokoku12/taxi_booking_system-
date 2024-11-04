import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
import random


# Clear all input fields and reset the checkbox
def clear():
    customerSignup_first_name_entry.delete(0, tk.END)
    customerSignup_last_name_entry.delete(0, tk.END)
    customerSignup_title_combobox.set('')
    customerSignup_age_spinbox.delete(0, tk.END)
    customerSignup_address_entry.delete(0, tk.END)
    customerSignup_email_entry.delete(0, tk.END)
    customerSignup_phoneNumber_entry.delete(0, tk.END)
    customerSignup_payment_method_combobox.set('')
    customerSignup_username_entry.delete(0, tk.END)
    customerSignup__password_entry.delete(0, tk.END)
    check.set(0)

def validate_phone_number(char):
    return char.isdigit()


def generate_booking_id():
    return random.randint(100, 999)

def is_booking_id_exists(booking_id, mycursor):
    query = 'SELECT COUNT(*) FROM customer_booking_data WHERE Booking_id = %s'
    mycursor.execute(query, (booking_id,))
    count = mycursor.fetchone()[0]
    return count > 0




def conenct_toCustomerdatabase():

    try:
        con = pymysql.connect(host='localhost', user='root', password='Neil12345.')
        mycursor = con.cursor()

    except:
        messagebox.showerror('Error', 'Data connectivity issue, try again')
        return None
    
    


    # Check if any of the required fields are empty and display a warning if so
    if (
        customerSignup_first_name_entry.get() == ''
        or customerSignup_last_name_entry.get() == ''
        or customerSignup_address_entry.get() == ''
        or customerSignup_email_entry.get() == ''
        or customerSignup_phoneNumber_entry.get() == ''
        or customerSignup_payment_method_combobox.get() == ''
        or customerSignup_username_entry.get() == ''
        or customerSignup__password_entry.get() == ''
    ):
        messagebox.showwarning("Account have been Created!", " all fields are required")
        
    # Check if the terms and conditions checkbox is not checked and display a warning if so
    elif check.get() == 0:
        messagebox.showwarning('Accept Term and condition!', 'Please Accept Term and condition!')
    else:
        try:
            # Attempt to connect to the database
            con = pymysql.connect(host='localhost', user='root', password='Neil12345.')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Data connectivity issue, try again')
            return

        try:
            # Try to create the database, switch to it, and create the 'customerdata' table
            query = 'create database if not exists customerdata'
            mycursor.execute(query)
            query = 'use customerdata'
            mycursor.execute(query)
            query = 'create table if not exists customerdata (user_id int auto_increment primary key not null, firstName varchar(20), lastName varchar(20), title varchar(20), age varchar(20), address varchar(20), email varchar(20), phoneNumber varchar(20), payment_method varchar(20), username varchar(20), password varchar(20))'
            mycursor.execute(query)
            con.commit()
        except:
            # If the database already exists, switch to it
            mycursor.execute('use customerdata')


        # Insert user data into the 'customerdata' table
        query = 'insert into customerdata (firstName, lastName, title, age, address, email, phoneNumber, payment_method, username, password) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        mycursor.execute(
            query,
            (
                
                customerSignup_first_name_entry.get(),
                customerSignup_last_name_entry.get(),
                customerSignup_title_combobox.get(),
                customerSignup_age_spinbox.get(),
                customerSignup_address_entry.get(),
                customerSignup_email_entry.get(),
                customerSignup_phoneNumber_entry.get(),
                customerSignup_payment_method_combobox.get(),
                customerSignup_username_entry.get(),
                customerSignup__password_entry.get(),
            ),
        )

        global current_user_id
        current_user_id = mycursor.lastrowid

        con.commit()
        con.close()
        # Display a success message and clear the input fields
        messagebox.showinfo('Success', 'Account created')
        clear()

def back_to_login():
    cutomer_creating_new_account.destroy()
    import TBS

# Create the main window
cutomer_creating_new_account = tk.Tk()
cutomer_creating_new_account.geometry('500x550')

# Create a frame for user info
customerSignup_user_info_frame = tk.LabelFrame(cutomer_creating_new_account, text="User information")
customerSignup_user_info_frame.grid(row=0, column=0, padx=20, pady=10, sticky="news")

# Create a frame for user contacts
customerSignup_user_contact_frame = tk.LabelFrame(cutomer_creating_new_account, text="User Contacts")
customerSignup_user_contact_frame.grid(row=1, column=0, padx=20, pady=10, sticky="news")

# Create a frame for user account
customerSignup_user_credential_frame = tk.LabelFrame(cutomer_creating_new_account, text="User Account")
customerSignup_user_credential_frame.grid(row=2, column=0, padx=20, pady=10, sticky="news")

# Create a frame for terms and conditions
customerSignup_term_frame = tk.LabelFrame(cutomer_creating_new_account, text="Terms & Conditions")
customerSignup_term_frame.grid(row=3, column=0, padx=20, pady=10, sticky="news")

# Add widgets to the user_info_frame using grid
customerSignup_first_name_label = tk.Label(customerSignup_user_info_frame, text="First Name")
customerSignup_first_name_label.grid(row=0, column=0)
customerSignup_first_name_entry = tk.Entry(customerSignup_user_info_frame)
customerSignup_first_name_entry.grid(row=1, column=0)

# last name labels
customerSignup_last_name_label = tk.Label(customerSignup_user_info_frame, text="Last Name")
customerSignup_last_name_label.grid(row=0, column=1)
customerSignup_last_name_entry = tk.Entry(customerSignup_user_info_frame)
customerSignup_last_name_entry.grid(row=1, column=1)

# title labels
customerSignup_title_label = tk.Label(customerSignup_user_info_frame, text="Title")
customerSignup_title_combobox = ttk.Combobox(customerSignup_user_info_frame, values=["", "Mr", "Ms", "DR"])
customerSignup_title_label.grid(row=0, column=2)
customerSignup_title_combobox.grid(row=1, column=2)

# age labels
customerSignup_age_label = tk.Label(customerSignup_user_info_frame, text="Age")
customerSignup_age_spinbox = tk.Spinbox(customerSignup_user_info_frame, from_=18, to=100)
customerSignup_age_label.grid(row=2, column=0)
customerSignup_age_spinbox.grid(row=3, column=0)

# address
customerSignup_address_label = tk.Label(customerSignup_user_info_frame, text="Address")
customerSignup_address_label.grid(row=2, column=1)
customerSignup_address_entry = tk.Entry(customerSignup_user_info_frame)
customerSignup_address_entry.grid(row=3, column=1)

# Add widgets to the user_contact_frame using grid
customerSignup_email_label = tk.Label(customerSignup_user_contact_frame, text="Email")
customerSignup_email_label.grid(row=0, column=1)
customerSignup_email_entry = tk.Entry(customerSignup_user_contact_frame)
customerSignup_email_entry.grid(row=1, column=1)

# phone number
customerSignup_phoneNumber_label = tk.Label(customerSignup_user_contact_frame, text="Phone Number")
validate_phone_number_cmd = (customerSignup_user_contact_frame.register(validate_phone_number), '%S')
customerSignup_phoneNumber_entry = tk.Entry(
    customerSignup_user_contact_frame, validate="key", validatecommand=validate_phone_number_cmd
)
customerSignup_phoneNumber_label.grid(row=0, column=2)
customerSignup_phoneNumber_entry.grid(row=1, column=2)

customerSignup_payment_method_label = tk.Label(customerSignup_user_contact_frame, text="Payment Method")
customerSignup_payment_method_combobox = ttk.Combobox(customerSignup_user_contact_frame, values=["", "Card", "Cash"])
customerSignup_payment_method_label.grid(row=0, column=3)
customerSignup_payment_method_combobox.grid(row=1, column=3)

# Add widgets to the user_credential_frame using grid
customerSignup_username_label = tk.Label(customerSignup_user_credential_frame, text="Username")
customerSignup_username_label.grid(row=0, column=1)
customerSignup_username_entry = tk.Entry(customerSignup_user_credential_frame)
customerSignup_username_entry.grid(row=1, column=1)

# customer password
customerSignup__password_label = tk.Label(customerSignup_user_credential_frame, text="Password")
customerSignup__password_label.grid(row=0, column=2)
customerSignup__password_entry = tk.Entry(customerSignup_user_credential_frame)
customerSignup__password_entry.grid(row=1, column=2)

# Add widgets to the term_frame using grid
check = tk.IntVar()
customerSignup_term_check = tk.Checkbutton(
    customerSignup_term_frame, text="I accept the term and conditions.", variable=check
)
customerSignup_term_check.grid(row=0, column=0)

# Create "Create Account" button
customerSignup_enterData_button = tk.Button(
    cutomer_creating_new_account, text="Create Account", font=("Arial", 16), command=conenct_toCustomerdatabase
)
customerSignup_enterData_button.grid(row=4, column=0, sticky="news", padx=10, pady=10)

customerSignup_enterDataLogin_button = tk.Button(
    cutomer_creating_new_account, text=" Login!", font=("Arial", 16), command=back_to_login
)
customerSignup_enterDataLogin_button.grid(row=5, column=0, sticky="news", padx=10, pady=10)

# Adjust padding for widgets in user_info_frame
for widget in customerSignup_user_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Adjust padding for widgets in user_contact_frame
for widget in customerSignup_user_contact_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Adjust padding for widgets in user_credential_frame
for widget in customerSignup_user_credential_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

cutomer_creating_new_account.mainloop()
