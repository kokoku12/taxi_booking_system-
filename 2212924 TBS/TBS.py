import tkinter as tk
from tkinter import messagebox
import pymysql
from bokingpanel import open_booking_panel
from driverpanel import DriverPanelApp
from adminpanel import admin_panel


# Global Variables this is the window for the aplication 
TBS_Home_root = tk.Tk()
TBS_Home_root.title('Taxi booking System')
TBS_Home_root.geometry('500x500')
TBS_Home_root.configure(bg='#333333')

# Functions

def customer_login_table():
    # Hide the main window
    TBS_Home_root.withdraw()
    def customer_login():
        # Check if both username and password fields are filled
        if costumer_username_entry.get() == '' or costumer_password_entry.get() == '':
            messagebox.showerror('Error', 'All fields are required')
        else:
            try:
                 # Attempt to establish a connection to the MySQL database
                customer_con = pymysql.connect(host='localhost', user='root', password='Neil12345.')
                mycursor = customer_con.cursor()
            except:
                 # Display an error message if the connection fails
                messagebox.showerror('Error', 'Connection is not established, try again')
                return
             # Select the 'customerdata' database
            query = 'use customerdata'
            mycursor.execute(query)

             # Check if the entered username and password match any records in the 'customerdata' table
            query = 'select * from customerdata where username=%s and password=%s'
            mycursor.execute(query, (costumer_username_entry.get(), costumer_password_entry.get()))
            cmrow = mycursor.fetchone()
            if cmrow is None:
                 # Display an error message for invalid password
                messagebox.showerror('Error', 'Invalid password')
            else:
                 # Display a success message and close the main window, then open the booking panel
                messagebox.showinfo('Welcome', 'Login successful')
                TBS_Home_root.destroy()
                open_booking_panel()
            
    
    def customer_create_account1():
        TBS_Home_root.destroy()
        import customer_signup

    # Create a new window for customer login
    costumer_window = tk.Toplevel(TBS_Home_root)
    costumer_window.title('Taxi booking System - Customer login')
    costumer_window.geometry('500x500')
    costumer_window.configure(bg='#333333')

    # Create a frame for customer login elements
    customer_login_table_frame = tk.Frame(costumer_window, bg='#333333')

    # Customer login labels, entry fields, and buttons
    costumer_login_label = tk.Label(customer_login_table_frame, text="Customer Login", bg='#333333', fg='#ffffff',
                                     font=("Arial", 30))
    costumer_username_label = tk.Label(customer_login_table_frame, text="Username", bg='#333333', fg='#ffffff',
                                       font=("Arial", 16))
    costumer_username_entry = tk.Entry(customer_login_table_frame, font=("Arial", 16))
    costumer_password_entry = tk.Entry(customer_login_table_frame, show="*", font=("Arial", 16))
    costumer_password_label = tk.Label(customer_login_table_frame, text="Password", bg='#333333', fg='#ffffff',
                                       font=("Arial", 16))
    costumer_login_button = tk.Button(customer_login_table_frame, text="Login", font=("Arial", 16),
                                      command=customer_login)
    costumer_create_account_button = tk.Button(customer_login_table_frame, text="Create Account", font=("Arial", 16),
                                               command=customer_create_account1)
  
    # Grid placement of customer login elements
    costumer_login_label.grid(row=0, column=0, columnspan=2, sticky='news', pady=40)
    costumer_username_label.grid(row=1, column=0)
    costumer_username_entry.grid(row=1, column=1, pady=20)
    costumer_password_label.grid(row=2, column=0)
    costumer_password_entry.grid(row=2, column=1, pady=20)
    costumer_login_button.grid(row=3, column=0, columnspan=2, pady=20)
    costumer_create_account_button.grid(row=4, column=0, columnspan=2, pady=20)

    customer_login_table_frame.pack()

def driver_login_table():
    TBS_Home_root.withdraw()
    def driver_login():
        if driver_username_entry.get() == '' or driver_password_entry.get() == '':
            messagebox.showerror('Error', 'All fields are required')
        else:
            try:
                driver_con = pymysql.connect(host='localhost', user='root', password='Neil12345.')
                mycursor = driver_con.cursor()
            except:
                messagebox.showerror('Error', 'Connection is not established, try again')
                return
            query = 'use driverdata'
            mycursor.execute(query)
            query = 'select * from driverdata where username=%s and password=%s'
            mycursor.execute(query, (driver_username_entry.get(), driver_password_entry.get()))
            cmrow = mycursor.fetchone()
            if cmrow is None:
                messagebox.showerror('Error', 'Invalid password')
            else:
                messagebox.showinfo('Welcome', 'Login successful')
                app = DriverPanelApp()

    def createDriver_account1():
        TBS_Home_root.destroy()
        import driver_signup

    driver_window = tk.Toplevel(TBS_Home_root)
    driver_window.title('Taxi booking System - Driver login')
    driver_window.geometry('500x500')
    driver_window.configure(bg='#333333')

    driver_login_table_frame = tk.Frame(driver_window, bg='#333333')

    driver_login_label = tk.Label(driver_login_table_frame, text="Driver Login", bg='#333333', fg='#ffffff',
                                  font=("Arial", 30))
    driver_username_label = tk.Label(driver_login_table_frame, text="Username", bg='#333333', fg='#ffffff',
                                     font=("Arial", 16))
    driver_username_entry = tk.Entry(driver_login_table_frame, font=("Arial", 16))
    driver_password_entry = tk.Entry(driver_login_table_frame, show="*", font=("Arial", 16))
    driver_password_label = tk.Label(driver_login_table_frame, text="Password", bg='#333333', fg='#ffffff',
                                     font=("Arial", 16))
    driver_login_button = tk.Button(driver_login_table_frame, text="Login", font=("Arial", 16), command=driver_login)
    driver_create_account_button = tk.Button(driver_login_table_frame, text="Create Account", font=("Arial", 16),
                                             command=createDriver_account1)

    driver_login_label.grid(row=0, column=0, columnspan=2, sticky='news', pady=40)
    driver_username_label.grid(row=1, column=0)
    driver_username_entry.grid(row=1, column=1, pady=20)
    driver_password_label.grid(row=2, column=0)
    driver_password_entry.grid(row=2, column=1, pady=20)
    driver_login_button.grid(row=3, column=0, columnspan=2, pady=20)
    driver_create_account_button.grid(row=4, column=0, columnspan=2, pady=20)

    driver_login_table_frame.pack()

def admin_login_table():
    # Hide the main window
    TBS_Home_root.withdraw()
    def admin_login():
        # Check if username or password fields are empty
        if admin_username_entry.get() == '' or admin_password_entry.get() == '':
            messagebox.showerror('Error', 'All fields are required')
        else:
            try:
                # Establish a connection to the database
                admin_con = pymysql.connect(host='localhost', user='root', password='Neil12345.')
                mycursor = admin_con.cursor()
            except:
                # Display an error message if the connection fails
                messagebox.showerror('Error', 'Connection is not established, try again')
                return
            # Use the 'admindata' database
            query = 'use admindata'
            mycursor.execute(query)

            # Check the admin credentials in the database
            query = 'select * from admindata where username=%s and password=%s'
            mycursor.execute(query, (admin_username_entry.get(), admin_password_entry.get()))
            cmrow = mycursor.fetchone()

            if cmrow is None:
                # Display an error message for invalid password
                messagebox.showerror('Error', 'Invalid password')
            else:
                # Display a success message and open the admin panel
                messagebox.showinfo('Welcome', 'Login successful')
                admin_panel()

    def adminSignup():
        # Destroy the main window and open the admin signup module
        TBS_Home_root.destroy()
        import admin_signup

    # Create a new window for admin login
    admin_window = tk.Toplevel(TBS_Home_root)
    admin_window.title('Taxi booking System - Admin login')
    admin_window.geometry('500x500')
    admin_window.configure(bg='#333333')

    # Create a frame for admin login elements
    admin_login_table_frame = tk.Frame(admin_window, bg='#333333')

    # Admin login labels, entry fields, and buttons
    admin_login_label = tk.Label(admin_login_table_frame, text="Admin Login", bg='#333333', fg='#ffffff',
                                 font=("Arial", 30))
    admin_username_label = tk.Label(admin_login_table_frame, text="Username", bg='#333333', fg='#ffffff',
                                    font=("Arial", 16))
    admin_username_entry = tk.Entry(admin_login_table_frame, font=("Arial", 16))
    admin_password_entry = tk.Entry(admin_login_table_frame, show="*", font=("Arial", 16))
    admin_password_label = tk.Label(admin_login_table_frame, text="Password", bg='#333333', fg='#ffffff',
                                    font=("Arial", 16))
    admin_login_button = tk.Button(admin_login_table_frame, text="Login", font=("Arial", 16), command=admin_login)
    admin_create_account_button = tk.Button(admin_login_table_frame, text="Create Account", font=("Arial", 16),
                                            command=adminSignup)

    # Grid placement of admin login elements
    admin_login_label.grid(row=0, column=0, columnspan=2, sticky='news', pady=40)
    admin_username_label.grid(row=1, column=0)
    admin_username_entry.grid(row=1, column=1, pady=20)
    admin_password_label.grid(row=2, column=0)
    admin_password_entry.grid(row=2, column=1, pady=20)
    admin_login_button.grid(row=3, column=0, columnspan=2, pady=20)
    admin_create_account_button.grid(row=4, column=0, columnspan=2, pady=20)

    admin_login_table_frame.pack()

# Widgets for the main window
welcome_label = tk.Label(TBS_Home_root, text="Welcome ", bg='#333333', fg='#ffffff', font=("Arial", 30))
welcome_label.grid(row=0, column=0, columnspan=2, sticky='news', pady=40)

main_customer_login = tk.Button(TBS_Home_root, text="Customer Login", font=("Arial", 16), command=customer_login_table)
main_customer_login.grid(row=1, column=0, columnspan=2, pady=20, padx=170)

main_driver_login = tk.Button(TBS_Home_root, text="Driver Login", font=("Arial", 16), command=driver_login_table)
main_driver_login.grid(row=2, column=0, columnspan=2, pady=20)

main_admin_login = tk.Button(TBS_Home_root, text="Admin Login", font=("Arial", 16), command=admin_login_table)
main_admin_login.grid(row=3, column=0, columnspan=2, pady=20)

# Main loop
TBS_Home_root.mainloop()
