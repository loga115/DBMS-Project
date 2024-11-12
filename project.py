import cx_Oracle
from datetime import datetime
import tkinter as tk
from tkinter import messagebox


# Connect to Oracle database
dsn_tns = cx_Oracle.makedsn("TUF_GAMING", "1521", service_name="XE")
db = cx_Oracle.connect(
    user=r"system", password="password", dsn=dsn_tns
)
cursor = db.cursor()


# Create GUI
class ParkingSystem:
    def __init__(self, master):
        self.master = master
        self.master.title("Parking System")

        # Create input frame
        self.input_frame = tk.Frame(self.master)
        self.input_frame.pack(pady=10)

        self.label_license_plate = tk.Label(self.input_frame, text="License Plate:")
        self.label_license_plate.grid(row=0, column=0, padx=(20, 0), pady=(0, 10))
        self.entry_license_plate = tk.Entry(self.input_frame, width=30)
        self.entry_license_plate.grid(row=0, column=1, padx=(0, 20), pady=(0, 10))

        self.label_owner_info = tk.Label(self.input_frame, text="Owner Info:")
        self.label_owner_info.grid(row=1, column=0, padx=(20, 0), pady=(0, 10))
        self.entry_owner_info = tk.Entry(self.input_frame, width=30)
        self.entry_owner_info.grid(row=1, column=1, padx=(0, 20), pady=(0, 10))

        self.button_park = tk.Button(self.input_frame, text="Park", command=self.park_vehicle)
        self.button_park.grid(row=2, column=0, columnspan=2, padx=(20, 0), pady=(0, 10))

        # Create output frame
        self.output_frame = tk.Frame(self.master)
        self.output_frame.pack(pady=10)

        self.label_parking_id = tk.Label(self.output_frame, text="Parking ID:")
        self.label_parking_id.grid(row=0, column=0, padx=(20, 0), pady=(0, 10))
        self.entry_parking_id = tk.Entry(self.output_frame, width=30)
        self.entry_parking_id.grid(row=0, column=1, padx=(0, 20), pady=(0, 10))

        self.label_fee = tk.Label(self.output_frame, text="Fee:")
        self.label_fee.grid(row=1, column=0, padx=(20, 0), pady=(0, 10))
        self.entry_fee = tk.Entry(self.output_frame, width=30, state="readonly")
        self.entry_fee.grid(row=1, column=1, padx=(0, 20), pady=(0, 10))

        self.button_unpark = tk.Button(self.output_frame, text="Unpark", command=self.unpark_vehicle)
        self.button_unpark.grid(row=2, column=0, columnspan=2, padx=(20, 0), pady=(0, 10))

        self.button_get_fee = tk.Button(self.output_frame, text="Get Fee", command=self.get_fee)
        self.button_get_fee.grid(row=3, column=0, columnspan=2, padx=(20, 0), pady=(0, 10))

    def park_vehicle(self):
        license_plate = self.entry_license_plate.get()
        owner_info = self.entry_owner_info.get()
        parking_id = cursor.var(int)
        slot_val = cursor.var(int)

        try:
            cursor.callproc("PV_ON_LP", [license_plate, owner_info, parking_id, slot_val])
            self.entry_parking_id.config(state="normal")
            self.entry_parking_id.delete(0, tk.END)
            self.entry_parking_id.insert(0, parking_id.getvalue())
            messagebox.showinfo("Vehicle Parked", f"Vehicle with Parking ID {parking_id.getvalue()} has been parked in Slot {slot_val.getvalue()}")

        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Error", str(e))

    def unpark_vehicle(self):
        parking_id = self.entry_parking_id.get()
        fee_val = cursor.var(int)
        try:
            cursor.callproc("RemoveVehicle", [parking_id, fee_val])
            self.entry_fee.config(state="normal")
            messagebox.showinfo("Vehicle Removed", f"Vehicle with Parking ID {parking_id} has been removed. Fee: {fee_val.getvalue()}")
            self.entry_fee.config(state="readonly")
        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Error", str(e))

    def get_fee(self):
        parking_id = self.entry_parking_id.get()
        entry_fee = cursor.var(int)

        try:
            cursor.callproc("ViewFee", [parking_id, entry_fee])
            self.entry_fee.config(state="normal")
            self.entry_fee.delete(0, tk.END)
            self.entry_fee.insert(0, entry_fee.getvalue())
            self.entry_fee.config(state="readonly")

        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Error", str(e))
    

# Create main window
root = tk.Tk()
app = ParkingSystem(root)
root.mainloop()

# Close connection
cursor.close()
db.close()