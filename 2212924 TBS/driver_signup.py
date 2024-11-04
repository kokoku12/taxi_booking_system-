import tkinter as tk
from tkinter import ttk, messagebox
import pymysql

# Clear all input fields and reset the checkbox
def clear():
    DriverSignup_first_name_entry.delete(0, tk.END)
    DriverSignup_last_name_entry.delete(0, tk.END)
    DriverSignup_title_combobox.delete(0, tk.END)
    DriverSignup_age_spinbox.delete(0, tk.END)
    DriverSignup_address_entry.delete(0, tk.END)
    DriverSignup_email_entry.delete(0, tk.END)
    DriverSignup_licenseNumber_entry.delete(0, tk.END)
    plateNumber_entry.delete(0, tk.END)
    DriverSignup_phoneNumber_entry.delete(0, tk.END)
    DriverSignup_username_entry.delete(0, tk.END)
    DriverSignup__password_entry.delete(0, tk.END)
    check.set(0)

def conenct_todriverdatabase():

     # Check if any of the required fields are empty and display a warning if so
    if DriverSignup_first_name_entry.get() =='' or DriverSignup_last_name_entry.get() == '' or DriverSignup_address_entry.get() == '' or  DriverSignup_email_entry.get() == '' or DriverSignup_phoneNumber_entry.get() == '' or DriverSignup_licenseNumber_entry.get() == ''or plateNumber_entry.get() == '' or DriverSignup_username_entry.get() == '' or DriverSignup__password_entry.get() == '':
        
        messagebox.showwarning("Account have been Created!", " all fields are required")

     # Check if the terms and conditions checkbox is not checked and display a warning if so
    elif check.get() == 0:
        messagebox.showwarning('Accept Term and condition!', 'Please Accept Term and condition!')

    else:
        try:
             # Attempt to connect to the database
            con = pymysql.connect(host= 'localhost', user='root', password='Neil12345.')
            mycursor = con.cursor()
        
        except:
            messagebox.showerror('Error','Data connectivity issue, try again')
            return
        
        try:
             # Try to create the database, switch to it, and create the 'driverdata' table
            query = 'create database driverdata'
            mycursor.execute(query)
            query = 'use driverdata'
            mycursor.execute(query)
            query = 'create table driverdata (id int auto_increment primary key not null, firstName varchar(20), lastName varchar(20), title varchar(20), age varchar(20), address varchar(20), email varchar(20), phoneNumber varchar(20), licenseNumber varchar(20), plateNumber varchar(20), username varchar(20), password varchar(20))'

            mycursor.execute(query)
        except:
            # If the database already exists, switch to it
            mycursor.execute('use driverdata')

        # Insert user data into the 'driverdata' table
        # Update the INSERT INTO statement
        query = 'insert into driverdata(firstName, lastName, title, age, address, email, phoneNumber, licenseNumber, plateNumber, username, password) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

        
        mycursor.execute(query, (
            DriverSignup_first_name_entry.get(),
            DriverSignup_last_name_entry.get(),
            DriverSignup_title_combobox.get(),
            DriverSignup_age_spinbox.get(),
            DriverSignup_address_entry.get(),
            DriverSignup_email_entry.get(),
            DriverSignup_phoneNumber_entry.get(),
            DriverSignup_licenseNumber_entry.get(),
            plateNumber_entry.get(),
            DriverSignup_username_entry.get(),
            DriverSignup__password_entry.get()))
        
        con.commit()
        con.close()
         # Display a success message and clear the input fields
        messagebox.showinfo ('Success', 'Account created')
        clear()


def back_to_login():
    driver_creating_new_account.destroy()
    import TBS


# Create the main window
driver_creating_new_account = tk.Tk()
driver_creating_new_account.geometry('500x600')


# Create a frame for user info
DriverSignup_user_info_frame = tk.LabelFrame(driver_creating_new_account, text="User information")
DriverSignup_user_info_frame.grid(row=0, column=0, padx=20, pady=10, sticky="news")

# Create a frame for user contacts
driverSignup_user_contact_frame = tk.LabelFrame(driver_creating_new_account, text="User Contacts")
driverSignup_user_contact_frame.grid(row=1, column=0, padx=20, pady=10, sticky="news")

# Create a frame for user account
DriverSignup_user_credential_frame = tk.LabelFrame(driver_creating_new_account, text="User Account")
DriverSignup_user_credential_frame.grid(row=2, column=0, padx=20, pady=10, sticky="news")

# Create a frame for terms and conditions
driverSignup_term_frame = tk.LabelFrame(driver_creating_new_account, text="Terms & Conditions")
driverSignup_term_frame.grid(row=3, column=0, padx=20, pady=10, sticky="news")

#------------------------------------------------------------------------------------------------------------#

# Add widgets to the user_info_frame using grid
DriverSignup_first_name_label = tk.Label(DriverSignup_user_info_frame, text="First Name")
DriverSignup_first_name_label.grid(row=0, column=0)
DriverSignup_first_name_entry = tk.Entry(DriverSignup_user_info_frame)
DriverSignup_first_name_entry.grid(row=1, column=0)

#last name labels
DriverSignup_last_name_label = tk.Label(DriverSignup_user_info_frame, text="Last Name")
DriverSignup_last_name_label.grid(row= 0 , column=1)
DriverSignup_last_name_entry = tk.Entry(DriverSignup_user_info_frame)
DriverSignup_last_name_entry.grid(row=1, column=1)

#title labels
DriverSignup_title_label = tk.Label(DriverSignup_user_info_frame, text="Title")
DriverSignup_title_combobox = ttk.Combobox (DriverSignup_user_info_frame, values= ["","Mr","Ms","DR"])
DriverSignup_title_label.grid(row=0, column=2)
DriverSignup_title_combobox.grid(row=1, column=2)

#age labels 
DriverSignup_age_label = tk.Label(DriverSignup_user_info_frame, text="Age")
DriverSignup_age_spinbox = tk.Spinbox(DriverSignup_user_info_frame, from_=18, to=100)
DriverSignup_age_label.grid(row=2, column=0)
DriverSignup_age_spinbox.grid(row=3, column=0)

#address
DriverSignup_address_label = tk.Label(DriverSignup_user_info_frame, text="Address")
DriverSignup_address_label.grid(row= 2 , column=1)
DriverSignup_address_entry = tk.Entry(DriverSignup_user_info_frame)
DriverSignup_address_entry.grid(row=3, column=1)

#------------------------------------------------------------------------------------------------------------------#

# Add widgets to the user_contact_frame using grid
DriverSignup_email_label = tk.Label(driverSignup_user_contact_frame, text="Email")
DriverSignup_email_label.grid(row=0, column=1)
DriverSignup_email_entry = tk.Entry(driverSignup_user_contact_frame)
DriverSignup_email_entry.grid(row=1, column=1)

#phone number
DriverSignup_phoneNumber_label= tk.Label(driverSignup_user_contact_frame, text="Phone Number")
DriverSignup_phoneNumber_label.grid(row=0, column=2)
DriverSignup_phoneNumber_entry = tk.Entry(driverSignup_user_contact_frame)
DriverSignup_phoneNumber_entry.grid(row=1, column=2)

#License Number

DriverSignup_licenseNumber_label = tk.Label(driverSignup_user_contact_frame, text="license Number")
DriverSignup_licenseNumber_entry = tk.Entry(driverSignup_user_contact_frame)
DriverSignup_licenseNumber_label.grid(row=0, column=3)
DriverSignup_licenseNumber_entry.grid(row=1, column=3)


#plate number
plateNumber_label= tk.Label(driverSignup_user_contact_frame, text="Plate Number")
plateNumber_entry = tk.Entry(driverSignup_user_contact_frame)
plateNumber_label.grid(row=2, column=1)
plateNumber_entry.grid(row=3, column=1)

#--------------------------------------------------------------------------------------------------------#

# Add widgets to the user_credential_frame using grid
DriverSignup_username_label = tk.Label(DriverSignup_user_credential_frame, text="Username")
DriverSignup_username_label.grid(row=0, column=1)
DriverSignup_username_entry = tk.Entry(DriverSignup_user_credential_frame)
DriverSignup_username_entry.grid(row=1, column=1)

#customer password
DriverSignup__password_label= tk.Label(DriverSignup_user_credential_frame, text="Password")
DriverSignup__password_label.grid(row=0, column=2)
DriverSignup__password_entry = tk.Entry(DriverSignup_user_credential_frame)
DriverSignup__password_entry.grid(row=1, column=2)

#----------------------------------------------------------------------------------------------------------#

# Add widgets to the term_frame using grid
check = tk.IntVar()
DriverSignup_term_check = tk.Checkbutton(driverSignup_term_frame, text="I accept the term and conditions.",variable=check)
DriverSignup_term_check.grid(row=0, column=0)


# Create "Create Account" button
DriverSignup_enterData_button = tk.Button(driver_creating_new_account, text="Create Account", font=("Arial", 16), command=conenct_todriverdatabase)
DriverSignup_enterData_button.grid(row=4, column=0, sticky="news", padx=10, pady=10)

DriverSignup_enterDataLogin_button = tk.Button (driver_creating_new_account, text=" Login!", font=("Arial", 16), command=back_to_login)
DriverSignup_enterDataLogin_button.grid(row=5, column=0, sticky="news", padx=10, pady=10)

#-------------------------------------------------------------------------------------------------------------------------------------------------#

# Adjust padding for widgets in user_info_frame
for widget in DriverSignup_user_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Adjust padding for widgets in user_contact_frame
for widget in driverSignup_user_contact_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Adjust padding for widgets in user_credential_frame
for widget in DriverSignup_user_credential_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

driver_creating_new_account.mainloop()
