import cx_Oracle
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import re

class HotelManagementApp:
    def __init__(self, master):
        self.master = master
        master.title("Hotel Management System")
        master.geometry("1000x800") 

        self.db_connection = None
        self.connect_to_db()

        if self.db_connection:
            self.create_widgets()
            

    def connect_to_db(self):
       
       password_file_path = 'Password.txt' 
       with open(password_file_path, 'r') as f:
            db_password = f.read().strip()
       self.db_connection = cx_Oracle.connect("System", db_password, "localhost:1521/XEPDB1")
            

    def create_widgets(self):
       
        main_frame = ttk.Frame(self.master)
        main_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(main_frame)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all")))

        self.inner_content_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_content_frame, anchor="nw")

        self.inner_content_frame.bind("<Configure>", self.on_frame_configure)


        # --- Customer ---
        customer_frame = ttk.LabelFrame(self.inner_content_frame, text="Customer Management")
        customer_frame.pack(padx=10, pady=10, fill="x") 

        tk.Label(customer_frame, text="Customer ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.customer_id_entry = tk.Entry(customer_frame)
        self.customer_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(customer_frame, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.customer_name_entry = tk.Entry(customer_frame)
        self.customer_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(customer_frame, text="Phone No:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.customer_phone_entry = tk.Entry(customer_frame)
        self.customer_phone_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        customer_frame.grid_columnconfigure(1, weight=1)

        customer_buttons_frame = ttk.Frame(customer_frame)

        ttk.Button(customer_frame, text="Add Customer", command=self.add_customer).grid(row=3, column=0, padx=5, pady=5)
        ttk.Button(customer_frame, text="View Customers", command=self.view_customers).grid(row=3, column=1, padx=5, pady=5)
        ttk.Button(customer_frame, text="Update Customer", command=self.update_customer).grid(row=4, column=0, padx=5, pady=5)
        ttk.Button(customer_frame, text="Delete Customer", command=self.delete_customer).grid(row=4, column=1, padx=5, pady=5)


        self.customer_tree = ttk.Treeview(self.inner_content_frame, columns=("ID", "Name", "Phone"), show="headings")
        self.customer_tree.heading("ID", text="Customer ID")
        self.customer_tree.heading("Name", text="Name")
        self.customer_tree.heading("Phone", text="Phone No")
        self.customer_tree.pack(padx=10, pady=10, fill="both", expand=True)

        # --- Room ---
        room_frame = ttk.LabelFrame(self.inner_content_frame, text="Room Management")
        room_frame.pack(padx=10, pady=10, fill="x")

        ttk.Button(room_frame, text="View Rooms", command=self.view_rooms).pack(padx=5, pady=5)

        self.room_tree = ttk.Treeview(self.inner_content_frame, columns=("RoomID", "Type", "NoOfBeds", "Price", "HasRoomService"), show="headings")
        self.room_tree.heading("RoomID", text="Room ID")
        self.room_tree.heading("Type", text="Type")
        self.room_tree.heading("NoOfBeds", text="No. of Beds")
        self.room_tree.heading("Price", text="Price")
        self.room_tree.heading("HasRoomService", text="Room Service")
        self.room_tree.pack(padx=10, pady=10, fill="both", expand=True)

        # --- Reservation ---
        reservation_frame = ttk.LabelFrame(self.inner_content_frame, text="Reservation Management")
        reservation_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(reservation_frame, text="Reservation ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.reservation_id_entry = tk.Entry(reservation_frame)
        self.reservation_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(reservation_frame, text="Customer ID:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.reservation_customer_id_entry = tk.Entry(reservation_frame)
        self.reservation_customer_id_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(reservation_frame, text="Room ID:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.reservation_room_id_entry = tk.Entry(reservation_frame)
        self.reservation_room_id_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(reservation_frame, text="Check-in Date (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.reservation_checkin_entry = tk.Entry(reservation_frame)
        self.reservation_checkin_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(reservation_frame, text="Check-out Date (YYYY-MM-DD):").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.reservation_checkout_entry = tk.Entry(reservation_frame)
        self.reservation_checkout_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        ttk.Button(reservation_frame, text="Add Reservation", command=self.add_reservation).grid(row=5, column=0, padx=5, pady=5)
        ttk.Button(reservation_frame, text="View Reservations", command=self.view_reservations).grid(row=5, column=1, padx=5, pady=5)
        ttk.Button(reservation_frame, text="Update Reservation", command=self.update_reservation).grid(row=6, column=0, padx=5, pady=5)
        ttk.Button(reservation_frame, text="Delete Reservation", command=self.delete_reservation).grid(row=6, column=1, padx=5, pady=5)

        reservation_frame.grid_columnconfigure(1, weight=1)

        self.reservation_tree = ttk.Treeview(self.inner_content_frame, columns=("ResID", "CustID", "RoomID", "Checkin", "Checkout"), show="headings")
        self.reservation_tree.heading("ResID", text="Reservation ID")
        self.reservation_tree.heading("CustID", text="Customer ID")
        self.reservation_tree.heading("RoomID", text="Room ID")
        self.reservation_tree.heading("Checkin", text="Check-in Date")
        self.reservation_tree.heading("Checkout", text="Check-out Date")
        self.reservation_tree.pack(padx=10, pady=10, fill="both", expand=True)

        # --- Payment ---
        payment_frame = ttk.LabelFrame(self.inner_content_frame, text="Payment Management")
        payment_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(payment_frame, text="Payment ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.payment_id_entry = tk.Entry(payment_frame)
        self.payment_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(payment_frame, text="Customer ID:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.payment_customer_id_entry = tk.Entry(payment_frame)
        self.payment_customer_id_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(payment_frame, text="Amount:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.payment_amount_entry = tk.Entry(payment_frame)
        self.payment_amount_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(payment_frame, text="Mode of Payment ID:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.payment_mode_of_payment_id_entry = tk.Entry(payment_frame)
        self.payment_mode_of_payment_id_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        

        ttk.Button(payment_frame, text="Add Payment", command=self.add_payment).grid(row=4, column=0, padx=5, pady=5)
        ttk.Button(payment_frame, text="View Payments", command=self.view_payments).grid(row=4, column=1, padx=5, pady=5)
        ttk.Button(payment_frame, text="Update Payment", command=self.update_payment).grid(row=5, column=0, padx=5, pady=5)
        ttk.Button(payment_frame, text="Delete Payment", command=self.delete_payment).grid(row=5, column=1, padx=5, pady=5)

        payment_frame.grid_columnconfigure(1, weight=1)

        self.payment_tree = ttk.Treeview(self.inner_content_frame, columns=("PayID", "CustID", "Amount", "ModePayID", "ModePayName"), show="headings")
        self.payment_tree.heading("PayID", text="Payment ID")
        self.payment_tree.heading("CustID", text="Customer ID")
        self.payment_tree.heading("Amount", text="Amount")
        self.payment_tree.heading("ModePayID", text="Mode of Payment ID")
        self.payment_tree.heading("ModePayName", text="Mode of Payment") 
        self.payment_tree.pack(padx=10, pady=10, fill="both", expand=True)


    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    # --- Customer CRUD  ---
    def add_customer(self):
        customer_id = self.customer_id_entry.get()
        name = self.customer_name_entry.get()
        phone_no = self.customer_phone_entry.get()

        if not all([customer_id, name, phone_no]):
            messagebox.showwarning("Input Error", "All customer fields are required!")
            return
        
        if not re.fullmatch(r"C\d{3}", customer_id):
            messagebox.showwarning("Invalid Input", "Customer ID must start with 'C' followed by exactly three digits (e.g., C021).")
            return

        if not re.fullmatch(r"[a-zA-Z\s.]+", name):
            messagebox.showwarning("Invalid Input", "Name can only contain letters and spaces.")
            return

        if not re.fullmatch(r"0\d{10}", phone_no):
            messagebox.showwarning("Invalid Input", "Phone Number must start with '0' and be exactly 11 digits long.")
            return
        


        try:
            cursor = self.db_connection.cursor()
            sql = "INSERT INTO Customer (CustomerID, Name, PhoneNo) VALUES (:1, :2, :3)"
            cursor.execute(sql, (customer_id, name, phone_no))
            self.db_connection.commit()
            messagebox.showinfo("Success", "Customer added successfully!")
            self.clear_customer_entries()
            self.view_customers() 
        except cx_Oracle.Error as e:
            error_obj, = e.args
            messagebox.showerror("Database Error", f"Error adding customer: {error_obj.message}")

    def clear_customer_entries(self):
        self.customer_id_entry.delete(0, tk.END)
        self.customer_name_entry.delete(0, tk.END)
        self.customer_phone_entry.delete(0, tk.END)

    def view_customers(self):
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item) 

        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT * FROM CUSTOMER")
            for row in cursor:
                self.customer_tree.insert("", "end", values=row)
        except cx_Oracle.Error as e:
            error_obj, = e.args
            messagebox.showerror("Database Error", f"Error viewing customers: {error_obj.message}")

    def update_customer(self):
        selected_item = self.customer_tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a customer to update.")
            return
        


        old_values = self.customer_tree.item(selected_item, 'values')
        old_customer_id = old_values[0]
        old_name = old_values[1]
        old_phone_no = old_values[2]

        new_name_entry = self.customer_name_entry.get()
        new_phone_no_entry = self.customer_phone_entry.get()

        
        
        if new_name_entry == '':
           new_name_entry  = old_name
        if new_phone_no_entry == '':
           new_phone_no_entry = old_phone_no
           
        if not re.fullmatch(r"C\d{3}", old_customer_id):
            messagebox.showwarning("Invalid Input", "Customer ID must start with 'C' followed by exactly three digits (e.g., C021).")
            return

        if not re.fullmatch(r"[a-zA-Z\s.]+", new_name_entry):
            messagebox.showwarning("Invalid Input", "Name can only contain letters and spaces.")
            return

        if not re.fullmatch(r"0\d{10}", new_phone_no_entry):
            messagebox.showwarning("Invalid Input", "Phone Number must start with '0' and be exactly 11 digits long.")
            return
           
        try:
            cursor = self.db_connection.cursor()
            sql = "UPDATE CUSTOMER SET Name = :1, PhoneNo = :2  WHERE CustomerID = :3"
            try:
                cursor.execute(sql, (new_name_entry, new_phone_no_entry, old_customer_id))
                self.db_connection.commit() 
                if cursor.rowcount > 0:
                    messagebox.showinfo("Success", "Customer updated successfully!")
                    self.clear_customer_entries()
                    self.view_customers() 
                else:
                    messagebox.showwarning("No Update", "No customer found with that ID or no changes made.")
            except cx_Oracle.Error as e:
             error_obj, = e.args 
             error_message = error_obj.message
             error_code = error_obj.code 
             messagebox.showerror("Database Error", f"Failed to execute query:\n{error_message}")
            
        except cx_Oracle.Error as e:
            error_obj, = e.args
            messagebox.showerror("Database Error", f"Error updating customer: {error_obj.message}")

    def delete_customer(self):
        selected_item = self.customer_tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a customer to delete.")
            return

        customer_id_to_delete = self.customer_tree.item(selected_item, 'values')[0]

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete customer ID: {customer_id_to_delete}?"):
            try:
                cursor = self.db_connection.cursor()
                sql = "DELETE FROM Customer WHERE CustomerID = :1"
                cursor.execute(sql, (customer_id_to_delete,))
                self.db_connection.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Success", "Customer deleted successfully!")
                    self.clear_customer_entries()
                    self.view_customers() 
                else:
                    messagebox.showwarning("No Delete", "No customer found with that ID.")
            except cx_Oracle.Error as e:
                error_obj, = e.args
                messagebox.showerror("Database Error", f"Error deleting customer: {error_obj.message}")



    # --- Room Operations ---
    def view_rooms(self):
        for item in self.room_tree.get_children():
            self.room_tree.delete(item) 

        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT RoomID, Type, NoOfBeds, Price, HasRoomService FROM Room") # Explicitly list columns
            for row in cursor:
                self.room_tree.insert("", "end", values=row)
        except cx_Oracle.Error as e:
            error_obj, = e.args
            messagebox.showerror("Database Error", f"Error viewing rooms: {error_obj.message}")

    # --- Reservation CRUD ---
    def add_reservation(self):
        res_id = self.reservation_id_entry.get()
        cust_id = self.reservation_customer_id_entry.get()
        room_id = self.reservation_room_id_entry.get()
        checkin_date = self.reservation_checkin_entry.get()
        checkout_date = self.reservation_checkout_entry.get()

        if not all([res_id, cust_id, room_id, checkin_date]):
            messagebox.showwarning("Input Error", "All reservation fields are required! (Except for Checkout unless finished)")
            return
        
        if not re.fullmatch(r"RES\d{3}", res_id):
            messagebox.showwarning("Invalid Input", "Reservation ID must start with 'RES' (e.g., RES021).")
            return
        
        if not re.fullmatch(r"C\d{3}", cust_id):
            messagebox.showwarning("Invalid Input", "Customer ID must start with 'C'  (e.g., C021).")
            return
        
        if not re.fullmatch(r"R\d{3}", room_id):
            messagebox.showwarning("Invalid Input", "Room ID must start with 'R'  (e.g., R020).")
            return

        try:
            cursor = self.db_connection.cursor()
            sql = "INSERT INTO Reservation (ReservationID, CustomerID, RoomID, CheckinDate, CheckoutDate) VALUES (:1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'), TO_DATE(:5, 'YYYY-MM-DD'))"
            cursor.execute(sql, (res_id, cust_id, room_id, checkin_date, checkout_date))
            self.db_connection.commit()
            messagebox.showinfo("Success", "Reservation added successfully!")
            self.clear_reservation_entries()
            self.view_reservations()
        except cx_Oracle.Error as e:
            error_obj, = e.args
            messagebox.showerror("Database Error", f"Error adding reservation: {error_obj.message}")

    def view_reservations(self):
        for item in self.reservation_tree.get_children():
            self.reservation_tree.delete(item)

        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT ReservationID, CustomerID, RoomID, TO_CHAR(CheckinDate, 'YYYY-MM-DD'), TO_CHAR(CheckoutDate, 'YYYY-MM-DD') FROM Reservation")
            for row in cursor:
                self.reservation_tree.insert("", "end", values=row)
        except cx_Oracle.Error as e:
            error_obj, = e.args
            messagebox.showerror("Database Error", f"Error viewing reservations: {error_obj.message}")

    def update_reservation(self):
        selected_item = self.reservation_tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a reservation to update.")
            return

        old_res_id = self.reservation_tree.item(selected_item, 'values')[0]
        old_cust_id = self.reservation_tree.item(selected_item, 'values')[1]
        old_room_id = self.reservation_tree.item(selected_item, 'values')[2]
        old_checkin_date = self.reservation_tree.item(selected_item, 'values')[3]
        old_checkout_date = self.reservation_tree.item(selected_item, 'values')[4]
        new_cust_id = self.reservation_customer_id_entry.get()
        new_room_id = self.reservation_room_id_entry.get()
        new_checkin_date = self.reservation_checkin_entry.get()
        new_checkout_date = self.reservation_checkout_entry.get()
        
        if new_cust_id == '': 
                new_cust_id = old_cust_id 
        if new_room_id == '': 
                new_room_id = old_room_id
        if new_checkin_date == '': 
                new_checkin_date = old_checkin_date
        if old_checkout_date == 'None':
            old_checkout_date = '';
        if  new_checkout_date == '': 
                new_checkout_date = old_checkout_date

        if not re.fullmatch(r"RES\d{3}", old_res_id):
            messagebox.showwarning("Invalid Input", "Reservation ID must start with 'RES' (e.g., RES021).")
            return
        
        if not re.fullmatch(r"C\d{3}", new_cust_id):
            messagebox.showwarning("Invalid Input", "Customer ID must start with 'C'  (e.g., C021).")
            return
        
        if not re.fullmatch(r"R\d{3}", new_room_id):
            messagebox.showwarning("Invalid Input", "Room ID must start with 'R'  (e.g., R021).")
            return
      
        try:
            cursor = self.db_connection.cursor()
            sql = "UPDATE Reservation SET CustomerID = :1, RoomID = :2, CheckinDate = TO_DATE(:3, 'YYYY-MM-DD'), CheckoutDate = TO_DATE(:4, 'YYYY-MM-DD') WHERE ReservationID = :5"
            

            cursor.execute(sql, (new_cust_id, new_room_id, new_checkin_date, new_checkout_date, old_res_id))
            self.db_connection.commit()
            if cursor.rowcount > 0:
                messagebox.showinfo("Success", "Reservation updated successfully!")
                self.clear_reservation_entries()
                self.view_reservations()
            else:
                messagebox.showwarning("No Update", "No reservation found with that ID or no changes made.")
        except cx_Oracle.Error as e:
            error_obj, = e.args
            messagebox.showerror("Database Error", f"Error updating reservation: {error_obj.message}")

    def delete_reservation(self):
        selected_item = self.reservation_tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a reservation to delete.")
            return

        res_id_to_delete = self.reservation_tree.item(selected_item, 'values')[0]

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete reservation ID: {res_id_to_delete}?"):
            try:
                cursor = self.db_connection.cursor()
                sql = "DELETE FROM Reservation WHERE ReservationID = :1"
                cursor.execute(sql, (res_id_to_delete,))
                self.db_connection.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Success", "Reservation deleted successfully!")
                    self.clear_reservation_entries()
                    self.view_reservations()
                else:
                    messagebox.showwarning("No Delete", "No reservation found with that ID.")
            except cx_Oracle.Error as e:
                error_obj, = e.args
                messagebox.showerror("Database Error", f"Error deleting reservation: {error_obj.message}")

    def clear_reservation_entries(self):
        self.reservation_id_entry.delete(0, tk.END)
        self.reservation_customer_id_entry.delete(0, tk.END)
        self.reservation_room_id_entry.delete(0, tk.END)
        self.reservation_checkin_entry.delete(0, tk.END)
        self.reservation_checkout_entry.delete(0, tk.END)

    # --- Payment CRUD ---
    def add_payment(self):
        payment_id = self.payment_id_entry.get()
        customer_id = self.payment_customer_id_entry.get()
        amount = self.payment_amount_entry.get()
        mode_pay_id = self.payment_mode_of_payment_id_entry.get()

        if not all([payment_id, customer_id, amount, mode_pay_id]):
            messagebox.showwarning("Input Error", "All payment fields are required!")
            return
        
        if not re.fullmatch(r"P\d{3}", payment_id):
            messagebox.showwarning("Invalid Input", "Payment ID must start with 'P' (e.g., P021).")
            return
        
        if not re.fullmatch(r"C\d{3}", customer_id):
            messagebox.showwarning("Invalid Input", "Customer ID must start with 'C (e.g., C021).")
            return
        
        if not re.fullmatch(r"^\d+$", amount):
            messagebox.showwarning("Invalid Input", "Amount Must Be Numbers")
            return
        
        if not re.fullmatch(r"MOP0\d{1}", mode_pay_id):
            messagebox.showwarning("Invalid Input", "Mode of Payment ID must start with 'MOP' and only within 1-4 (e.g., MOP01).")
            return
        
        

        try:
            amount_float = float(amount) 
            cursor = self.db_connection.cursor()
            sql = "INSERT INTO Payment (PaymentID, CustomerID, Amount, ModeOfPaymentID) VALUES (:1, :2, :3, :4)"
            cursor.execute(sql, (payment_id, customer_id, amount_float, mode_pay_id))
            self.db_connection.commit()
            messagebox.showinfo("Success", "Payment added successfully!")
            self.clear_payment_entries()
            self.view_payments()
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a valid number!")
        except cx_Oracle.Error as e:
            error_obj, = e.args
            messagebox.showerror("Database Error", f"Error adding payment: {error_obj.message}")

    def view_payments(self):
        for item in self.payment_tree.get_children():
            self.payment_tree.delete(item)

        try:
            cursor = self.db_connection.cursor()
            cursor.execute("""
                SELECT
                    p.PaymentID,
                    p.CustomerID,
                    p.Amount,
                    p.ModeOfPaymentID,
                    m.Type
                FROM
                    Payment p
                JOIN
                    ModeOfPayment m ON p.ModeOfPaymentID = m.ModeOfPaymentID
            """)
            for row in cursor:
                self.payment_tree.insert("", "end", values=row)
        except cx_Oracle.Error as e:
            error_obj, = e.args
            messagebox.showerror("Database Error", f"Error viewing payments: {error_obj.message}")

    def update_payment(self):
        selected_item = self.payment_tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a payment to update.")
            return

        old_values = self.payment_tree.item(selected_item, 'values')
        old_payment_id = old_values[0]
        old_customer_id = old_values[1]
        old_amount = old_values[2]
        old_mode_pay_id = old_values[3] 

        new_customer_id_entry = self.payment_customer_id_entry.get()
        new_amount_entry = self.payment_amount_entry.get()
        new_mode_pay_id_entry = self.payment_mode_of_payment_id_entry.get()
        
        if new_customer_id_entry == '':
                new_customer_id_entry = old_customer_id
        if new_amount_entry == '':
                new_amount_entry = old_amount
        if new_mode_pay_id_entry == '':
                new_mode_pay_id_entry = old_mode_pay_id

        if not re.fullmatch(r"P\d{3}", old_payment_id):
            messagebox.showwarning("Invalid Input", "Payment ID must start with 'P' (e.g., P021).")
            return
        
        if not re.fullmatch(r"C\d{3}", new_customer_id_entry):
            messagebox.showwarning("Invalid Input", "Customer ID must start with 'C (e.g., C021).")
            return
        
        if not re.fullmatch(r"^\d+(\.\d+)?$", new_amount_entry):
            messagebox.showwarning("Invalid Input", "Amount Must Be Numbers")
            return
        
        if not re.fullmatch(r"MOP0\d{1}", new_mode_pay_id_entry):
            messagebox.showwarning("Invalid Input", "Mode of Payment ID must start with 'MOP' and only within 1-4 (e.g., MOP01).")
            return
        
        try:
            cursor = self.db_connection.cursor()
            sql = "UPDATE Payment SET CustomerID = :1, Amount = :2, ModeOfPaymentID = :3 WHERE PaymentID = :4"
            
           

            cursor.execute(sql, (new_customer_id_entry, new_amount_entry, new_mode_pay_id_entry, old_payment_id))
            self.db_connection.commit()
            if cursor.rowcount > 0:
                messagebox.showinfo("Success", "Payment updated successfully!")
                self.clear_payment_entries()
                self.view_payments()
            else:
                messagebox.showwarning("No Update", "No payment found with that ID or no changes made.")
        
        except cx_Oracle.Error as e:
            error_obj, = e.args
            messagebox.showerror("Database Error", f"Error updating payment: {error_obj.message}")

    def delete_payment(self):
        selected_item = self.payment_tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a payment to delete.")
            return

        payment_id_to_delete = self.payment_tree.item(selected_item, 'values')[0]

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete payment ID: {payment_id_to_delete}?"):
            try:
                cursor = self.db_connection.cursor()
                sql = "DELETE FROM Payment WHERE PaymentID = :1"
                cursor.execute(sql, (payment_id_to_delete,))
                self.db_connection.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Success", "Payment deleted successfully!")
                    self.clear_payment_entries()
                    self.view_payments()
                else:
                    messagebox.showwarning("No Delete", "No payment found with that ID.")
            except cx_Oracle.Error as e:
                error_obj, = e.args
                messagebox.showerror("Database Error", f"Error deleting payment: {error_obj.message}")

    def clear_payment_entries(self):
        self.payment_id_entry.delete(0, tk.END)
        self.payment_customer_id_entry.delete(0, tk.END)
        self.payment_amount_entry.delete(0, tk.END)
        self.payment_mode_of_payment_id_entry.delete(0, tk.END)

    def on_closing(self):
        if self.db_connection:
            self.db_connection.close()
            print("Database connection closed.")
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelManagementApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing) 
    root.mainloop()