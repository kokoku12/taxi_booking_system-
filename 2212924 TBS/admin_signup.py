import tkinter as tk
from tkinter import ttk, messagebox
import pymysql

# Clear all input fields and reset the checkbox
def clear():
    adminSignup_first_name_entry.delete(0, tk.END)
    adminSignup_last_name_entry.delete(0, tk.END)
    adminSignup_title_combobox.delete(0, tk.END)
    adminSignup_age_spinbox.delete(0, tk.END)
    adminSignup_address_entry.delete(0, tk.END)
    adminSignup_email_entry.delete(0, tk.END)
    adminSignup_phoneNumber_entry.delete(0, tk.END)
    adminSignup_username_entry.delete(0, tk.END)
    adminSignup__password_entry.delete(0, tk.END)
    check.set(0)





def conenct_toadmindatabase():
     # Check if any of the required fields are empty and display a warning if so
    if adminSignup_first_name_entry.get() =='' or adminSignup_last_name_entry.get() == '' or adminSignup_address_entry.get() == '' or  adminSignup_email_entry.get() == '' or adminSignup_phoneNumber_entry.get() == '' or adminSignup_username_entry.get() == '' or adminSignup__password_entry.get() == '':
        
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
             # Try to create the database, switch to it, and create the 'AdminData' table
            query = 'create database admindata'
            mycursor.execute(query)
            query = 'use admindata'
            mycursor.execute(query)
            query = 'create table AdminData (id int auto_increment primary key not null, firstName varchar(20), lastName varchar(20), title varchar(20), age varchar(20), address varchar(20), email varchar(20), phoneNumber varchar(20), username varchar(20), password varchar(20))'
            mycursor.execute(query)
        except:
            # If the database already exists, switch to it
            mycursor.execute('use admindata')

        # Insert user data into the 'AdminData' table
        query = 'insert into admindata(firstName, lastName, title, age, address, email, phoneNumber, username, password) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        mycursor.execute(query, (
            adminSignup_first_name_entry.get(),
            adminSignup_last_name_entry.get(),
            adminSignup_title_combobox.get(),
            adminSignup_age_spinbox.get(),
            adminSignup_address_entry.get(),
            adminSignup_email_entry.get(),
            adminSignup_phoneNumber_entry.get(),
            adminSignup_username_entry.get(),
            adminSignup__password_entry.get()))
        
        con.commit()
        con.close()
         # Display a success message and clear the input fields
        messagebox.showinfo ('Success', 'Account created')
        clear()

def back_to_login():
    admin_creating_new_account.withdraw()
    import TBS



# Create the main window
admin_creating_new_account = tk.Tk()
admin_creating_new_account.geometry('500x600')

# Create a frame for user info
adminSignup_user_info_frame = tk.LabelFrame(admin_creating_new_account, text="User information")
adminSignup_user_info_frame.grid(row=0, column=0, padx=20, pady=10, sticky="news")

# Create a frame for user contacts
adminSignup_user_contact_frame = tk.LabelFrame(admin_creating_new_account, text="User Contacts")
adminSignup_user_contact_frame.grid(row=1, column=0, padx=20, pady=10, sticky="news")

# Create a frame for user account
adminSignup_user_credential_frame = tk.LabelFrame(admin_creating_new_account, text="User Account")
adminSignup_user_credential_frame.grid(row=2, column=0, padx=20, pady=10, sticky="news")

# Create a frame for terms and conditions
adminSignup_term_frame = tk.LabelFrame(admin_creating_new_account, text="Terms & Conditions")
adminSignup_term_frame.grid(row=3, column=0, padx=20, pady=10, sticky="news")

#------------------------------------------------------------------------------------------------------------#

# Add widgets to the user_info_frame using grid
adminSignup_first_name_label = tk.Label(adminSignup_user_info_frame, text="First Name")
adminSignup_first_name_label.grid(row=0, column=0)
adminSignup_first_name_entry = tk.Entry(adminSignup_user_info_frame)
adminSignup_first_name_entry.grid(row=1, column=0)

#last name labels
adminSignup_last_name_label = tk.Label(adminSignup_user_info_frame, text="Last Name")
adminSignup_last_name_label.grid(row= 0 , column=1)
adminSignup_last_name_entry = tk.Entry(adminSignup_user_info_frame)
adminSignup_last_name_entry.grid(row=1, column=1)

#title labels
adminSignup_title_label = tk.Label(adminSignup_user_info_frame, text="Title")
adminSignup_title_combobox = ttk.Combobox (adminSignup_user_info_frame, values= ["","Mr","Ms","DR"])
adminSignup_title_label.grid(row=0, column=2)
adminSignup_title_combobox.grid(row=1, column=2)

#age labels 
adminSignup_age_label = tk.Label(adminSignup_user_info_frame, text="Age")
adminSignup_age_spinbox = tk.Spinbox(adminSignup_user_info_frame, from_=18, to=100)
adminSignup_age_label.grid(row=2, column=0)
adminSignup_age_spinbox.grid(row=3, column=0)

#address
adminSignup_address_label = tk.Label(adminSignup_user_info_frame, text="Address")
adminSignup_address_label.grid(row= 2 , column=1)
adminSignup_address_entry = tk.Entry(adminSignup_user_info_frame)
adminSignup_address_entry.grid(row=3, column=1)

#------------------------------------------------------------------------------------------------------------------#

# Add widgets to the user_contact_frame using grid
adminSignup_email_label = tk.Label(adminSignup_user_contact_frame, text="Email")
adminSignup_email_label.grid(row=0, column=1)
adminSignup_email_entry = tk.Entry(adminSignup_user_contact_frame)
adminSignup_email_entry.grid(row=1, column=1)

#phone number
adminSignup_phoneNumber_label= tk.Label(adminSignup_user_contact_frame, text="Phone Number")
adminSignup_phoneNumber_label.grid(row=0, column=2)
adminSignup_phoneNumber_entry = tk.Entry(adminSignup_user_contact_frame)
adminSignup_phoneNumber_entry.grid(row=1, column=2)

#--------------------------------------------------------------------------------------------------------#

# Add widgets to the user_credential_frame using grid
adminSignup_username_label = tk.Label(adminSignup_user_credential_frame, text="Username")
adminSignup_username_label.grid(row=0, column=1)
adminSignup_username_entry = tk.Entry(adminSignup_user_credential_frame)
adminSignup_username_entry.grid(row=1, column=1)

#customer password
adminSignup__password_label= tk.Label(adminSignup_user_credential_frame, text="Password")
adminSignup__password_label.grid(row=0, column=2)
adminSignup__password_entry =tk.Entry(adminSignup_user_credential_frame)
adminSignup__password_entry.grid(row=1, column=2)

#----------------------------------------------------------------------------------------------------------#

# Add widgets to the term_frame using grid

check = tk.IntVar()
adminSignup_term_check = tk.Checkbutton(adminSignup_term_frame, text="I accept the term and conditions.",variable=check)
adminSignup_term_check.grid(row=0, column=0)


# Create "Create Account" button
adminSignup_enterData_button = tk.Button(admin_creating_new_account, text="Create Account", font=("Arial", 16), command=conenct_toadmindatabase)
adminSignup_enterData_button.grid(row=4, column=0, sticky="news", padx=10, pady=10)

adminSignup_enterDataLogin_button = tk.Button (admin_creating_new_account, text=" Login!", font=("Arial", 16), command=back_to_login)
adminSignup_enterDataLogin_button.grid(row=5, column=0, sticky="news", padx=10, pady=10)

#-------------------------------------------------------------------------------------------------------------------------------------------------#

# Adjust padding for widgets in user_info_frame
for widget in adminSignup_user_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Adjust padding for widgets in user_contact_frame
for widget in adminSignup_user_contact_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Adjust padding for widgets in user_credential_frame
for widget in adminSignup_user_credential_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

admin_creating_new_account.mainloop()
