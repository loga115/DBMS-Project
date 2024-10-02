import cx_Oracle
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
from automatic_parking import detect_plate
import time

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
        self.master.title("Parking System Organizer")
        self.master.configure(bg="light blue")

        # Create welcome label
        self.label_welcome = tk.Label(self.master, text="Welcome to Parking System Organizer", font=("Arial", 16, "bold"), bg="light blue")
        self.label_welcome.pack(pady=20)

        # Create buttons frame
        self.buttons_frame = tk.Frame(self.master, bg="light blue")
        self.buttons_frame.pack()

        # Create park vehicle button
        self.button_park_vehicle = tk.Button(self.buttons_frame, text="Park Vehicle", font=("Arial", 12), command=self.open_park_vehicle_window)
        self.button_park_vehicle.pack(pady=10)

        # Create remove vehicle button
        self.button_remove_vehicle = tk.Button(self.buttons_frame, text="Remove Vehicle", font=("Arial", 12), command=self.open_remove_vehicle_window)
        self.button_remove_vehicle.pack(pady=10)

        # Create view car button
        self.button_view_car = tk.Button(self.buttons_frame, text="View Car", font=("Arial", 12), command=self.open_view_car_window)
        self.button_view_car.pack(pady=10)

    def open_park_vehicle_window(self):
        # Calculate the width and height of the window
        self.master.withdraw()
        # Create park vehicle window
        park_vehicle_window = tk.Toplevel(self.master)
        park_vehicle_window.title("Park Vehicle")
        park_vehicle_window.configure(bg="light blue")

        screen_width = park_vehicle_window.winfo_screenwidth()
        screen_height = park_vehicle_window.winfo_screenheight()
        window_width = int(screen_width * 0.3)
        window_height = int(screen_height * 0.3)

        # Calculate the x and y coordinates to center the window
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # Set the window size and position
        park_vehicle_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Create back button
        back_button = tk.Button(park_vehicle_window, text="Back", font=("Arial", 12), command=lambda: [park_vehicle_window.destroy(), self.master.deiconify()])
        back_button.pack(pady=10)

        # Create automatic parking button
        automatic_parking_button = tk.Button(park_vehicle_window, text="Automatic Parking", font=("Arial", 12), command=lambda: [park_vehicle_window.withdraw(), self.open_autom_parking_window()])
        automatic_parking_button.pack(pady=10)

        # Create manual parking button
        manual_parking_button = tk.Button(park_vehicle_window, text="Manual Parking", font=("Arial", 12), command=lambda: [park_vehicle_window.withdraw(), self.open_manual_parking_window()])
        manual_parking_button.pack(pady=10)

    def open_manual_parking_window(self):
        # Create manual parking window
        manual_parking_window = tk.Toplevel(self.master)
        manual_parking_window.title("Manual Parking")
        manual_parking_window.configure(bg="light blue")

        # Calculate the width and height of the window
        screen_width = manual_parking_window.winfo_screenwidth()
        screen_height = manual_parking_window.winfo_screenheight()
        window_width = int(screen_width * 0.3)
        window_height = int(screen_height * 0.3)

        # Calculate the x and y coordinates to center the window
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # Set the window size and position
        manual_parking_window.geometry(f"{window_width+30}x{window_height+30}+{x}+{y}")

        # Create back button
        back_button = tk.Button(manual_parking_window, text="Back", font=("Arial", 12), command=lambda: [manual_parking_window.withdraw(), self.open_park_vehicle_window()])
        back_button.pack(pady=10)

        # Create input frame
        self.input_frame = tk.Frame(manual_parking_window, bg="light blue")
        self.input_frame.pack(pady=10)

        self.label_license_plate = tk.Label(self.input_frame, text="License Plate:", font=("Arial", 12), bg="light blue")
        self.label_license_plate.grid(row=0, column=0, padx=(20, 0), pady=(0, 10))
        self.entry_license_plate = tk.Entry(self.input_frame, width=30)
        self.entry_license_plate.grid(row=0, column=1, padx=(0, 20), pady=(0, 10))

        self.label_owner_info = tk.Label(self.input_frame, text="Owner Info:", font=("Arial", 12), bg="light blue")
        self.label_owner_info.grid(row=1, column=0, padx=(20, 0), pady=(0, 10))
        self.entry_owner_info = tk.Entry(self.input_frame, width=30)
        self.entry_owner_info.grid(row=1, column=1, padx=(0, 20), pady=(0, 10))

        self.button_park = tk.Button(self.input_frame, text="Park", font=("Arial", 12), command=self.park_vehicle)
        self.button_park.grid(row=2, column=0, columnspan=2, padx=(20, 0), pady=(0, 10))

        # Create output frame
        self.output_frame = tk.Frame(manual_parking_window, bg="light blue")
        self.output_frame.pack(pady=10)

        self.label_parking_id = tk.Label(self.output_frame, text="Parking ID:", font=("Arial", 12), bg="light blue")
        self.label_parking_id.grid(row=0, column=0, padx=(20, 0), pady=(0, 10))
        self.entry_parking_id = tk.Entry(self.output_frame, width=30)
        self.entry_parking_id.grid(row=0, column=1, padx=(0, 20), pady=(0, 10))

    def open_autom_parking_window(self):
        # Create automatic parking window
        automatic_parking_window = tk.Toplevel(self.master)
        automatic_parking_window.title("Automatic Parking")
        automatic_parking_window.configure(bg="light blue")
        

        # Calculate the width and height of the window
        screen_width = automatic_parking_window.winfo_screenwidth()
        screen_height = automatic_parking_window.winfo_screenheight()
        window_width = int(screen_width * 0.3)
        window_height = int(screen_height * 0.3)

        # Calculate the x and y coordinates to center the window
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # Set the window size and position
        automatic_parking_window.geometry(f"{window_width+30}x{window_height+100}+{x}+{y}")

        # Create camera frame
        camera_frame = tk.Frame(automatic_parking_window, bg="light blue")
        camera_frame.pack(pady=10)

        # Create camera label
        camera_label = tk.Label(camera_frame, text="Camera Output", font=("Arial", 12), bg="light blue")
        camera_label.grid(row=0, column=0, columnspan=2)

        entry_license_plate_label_fr = tk.Label(camera_frame, text="Please keep the image steady while photo is taken..", font=("Arial", 12), bg="light blue")
        entry_license_plate_label_fr.grid(row=1, column=0, columnspan=2, pady=10)

        entry_license_plate_label = tk.Label(camera_frame, text="License Plate:", font=("Arial", 12), bg="light blue")
        entry_license_plate_label.grid(row=2, column=0, pady=10)

        # Create license plate entry box
        entry_license_plate = tk.Entry(camera_frame, width=30)
        entry_license_plate.grid(row=2, column=1, pady=10)



        # Create back button
        # TODO: Add code for camera output
        # Use OpenCV to capture camera output
        cap = cv2.VideoCapture(1)

        def show_camera_output():
            ret, frame = cap.read()
            if ret:
                # Convert the frame to RGB format
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Convert the frame to PIL Image format
                image = Image.fromarray(frame_rgb)

                # Resize the image to fit the label
                image = image.resize((400, 300))

                # Convert the image to PhotoImage format
                photo = ImageTk.PhotoImage(image)

                # Update the camera label with the new image
                camera_label.configure(image=photo)
                camera_label.image = photo

                # Call this function again after 10 milliseconds
                camera_label.after(10, show_camera_output)
            else:
                # Release the camera and destroy the window if capturing fails
                cap.release()
                # cv2.destroyAllWindows()
        


        back_button = tk.Button(automatic_parking_window, text="Back", font=("Arial", 12), command=lambda: [automatic_parking_window.destroy(), self.master.deiconify(), cap.release(), cv2.destroyAllWindows()])
        back_button.pack(pady=10)
        # Start showing the camera output
        show_camera_output()
        self.label_countdown = tk.Label(automatic_parking_window, text=str(5), font=("Arial", 12), bg="light blue")
        self.label_countdown.pack(pady=10)
        # TODO: Add code to count from 5 seconds and take a photo
        def take_photo():
            for i in range(3, 0, -1):
                self.label_countdown.configure(text=str(i))
                self.label_countdown.update()
                time.sleep(1)
                
            ret, frame = cap.read()
            if ret:
                # Save the frame to a file
                cv2.imwrite("photo.jpg", frame)
            else:
                messagebox.showerror("Error", "Failed to capture photo")
                automatic_parking_window.destroy()
                self.master.deiconify()
                cap.release()
                # cv2.destroyAllWindows()
            self.label_countdown.configure(text="")
            self.label_countdown.update()
            frame = cv2.imread("photo.jpg")
            license_plate = detect_plate(frame)
            if license_plate:
                    messagebox.showinfo("License Plate", f"License Plate: {license_plate}")
            else:
                    messagebox.showerror("Error", "License Plate not detected")
            
            if license_plate:
                entry_license_plate.insert(0, license_plate)
                self.park_vehicle_lp(license_plate)
                automatic_parking_window.destroy()
                self.master.deiconify()
                cap.release()
                # cv2.destroyAllWindows()
            else:
                messagebox.showerror("Error", "License Plate not detected")
                automatic_parking_window.destroy()
                self.master.deiconify()
                cap.release()
                cv2.destroyAllWindows()


        take_photo()
    
    def open_remove_vehicle_window(self):
        # Create remove vehicle window
        self.master.withdraw()
        remove_vehicle_window = tk.Toplevel(self.master)
        remove_vehicle_window.title("Remove Vehicle")
        remove_vehicle_window.configure(bg="light blue")
 
        # Calculate the width and height of the window
        screen_width = remove_vehicle_window.winfo_screenwidth()
        screen_height = remove_vehicle_window.winfo_screenheight()
        window_width = int(screen_width * 0.3)
        window_height = int(screen_height * 0.3)

        # Calculate the x and y coordinates to center the window
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # Set the window size and position
        remove_vehicle_window.geometry(f"{window_width+30}x{window_height+30}+{x}+{y}")
        

        # Create output frame
        self.output_frame = tk.Frame(remove_vehicle_window, bg="light blue")
        self.output_frame.pack(pady=10)

        self.label_parking_id = tk.Label(self.output_frame, text="Parking ID:", font=("Arial", 12), bg="light blue")
        self.label_parking_id.grid(row=0, column=0, padx=(20, 0), pady=(0, 10))
        self.entry_parking_id = tk.Entry(self.output_frame, width=30)
        self.entry_parking_id.grid(row=0, column=1, padx=(0, 20), pady=(0, 10))

        self.label_fee = tk.Label(self.output_frame, text="Fee:", font=("Arial", 12), bg="light blue")
        self.label_fee.grid(row=1, column=0, padx=(20, 0), pady=(0, 10))
        self.entry_fee = tk.Entry(self.output_frame, width=30, state="readonly")
        self.entry_fee.grid(row=1, column=1, padx=(0, 20), pady=(0, 10))


        # Create back button
        self.button_unpark = tk.Button(self.output_frame, text="Unpark", font=("Arial", 12), command=self.unpark_vehicle)
        self.button_unpark.grid(row=2, column=0, columnspan=2, padx=(20, 0), pady=(0, 10))

        back_button = tk.Button(remove_vehicle_window, text="Back", font=("Arial", 12), command=lambda: [remove_vehicle_window.destroy(), self.master.deiconify()])
        back_button.pack(pady=10)


    def open_view_car_window(self):
        # Create view car window
        self.master.withdraw()
        view_car_window = tk.Toplevel(self.master)
        view_car_window.title("View Car")
        view_car_window.configure(bg="light blue")

           
        # Calculate the width and height of the window
        screen_width = view_car_window.winfo_screenwidth()
        screen_height = view_car_window.winfo_screenheight()
        window_width = int(screen_width * 0.5)
        window_height = int(screen_height * 0.3)

        # Calculate the x and y coordinates to center the window
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        
        view_car_window.geometry(f"{window_width+30}x{window_height+30}+{x}+{y}")

        # Create output frame
        self.output_frame = tk.Frame(view_car_window, bg="light blue")
        self.output_frame.pack(pady=10)


        self.label_parking_id = tk.Label(self.output_frame, text="Parking ID:", font=("Arial", 12), bg="light blue")
        self.label_parking_id.grid(row=0, column=0, padx=(20, 0), pady=(0, 10))
        self.entry_parking_id = tk.Entry(self.output_frame, width=30)
        self.entry_parking_id.grid(row=0, column=1, padx=(0, 20), pady=(0, 10))

        self.label_license_plate = tk.Label(self.output_frame, text="License Plate:", font=("Arial", 12), bg="light blue")
        self.label_license_plate.grid(row=1, column=0, padx=(20, 0), pady=(0, 10))
        self.entry_license_plate = tk.Entry(self.output_frame, width=30)
        self.entry_license_plate.grid(row=1, column=1, padx=(0, 20), pady=(0, 10))

        self.label_fee = tk.Label(self.output_frame, text="Fee:", font=("Arial", 12), bg="light blue")
        self.label_fee.grid(row=7, column=0, padx=(20, 0), pady=(0, 10))
        self.entry_fee = tk.Entry(self.output_frame, width=30, state="readonly")
        self.entry_fee.grid(row=7, column=1, padx=(0, 20), pady=(0, 10))



        self.label_vehicle_name = tk.Label(self.output_frame, text="Vehicle Name:", font=("Arial", 12), bg="light blue")
        self.label_vehicle_name.grid(row=2, column=0, padx=(20, 0), pady=(0, 10))
        self.entry_vehicle_name = tk.Entry(self.output_frame, width=30)
        self.entry_vehicle_name.grid(row=2, column=1, padx=(0, 20), pady=(0, 10))
        self.entry_vehicle_name.config(state="readonly")

        self.label_vehicle_company = tk.Label(self.output_frame, text="Vehicle Company:", font=("Arial", 12), bg="light blue")
        self.label_vehicle_company.grid(row=3, column=0, padx=(20, 0), pady=(0, 10))
        self.entry_vehicle_company = tk.Entry(self.output_frame, width=30)
        self.entry_vehicle_company.grid(row=3, column=1, padx=(0, 20), pady=(0, 10))
        self.entry_vehicle_company.config(state="readonly")

        self.label_vehicle_type = tk.Label(self.output_frame, text="Vehicle Type:", font=("Arial", 12), bg="light blue")
        self.label_vehicle_type.grid(row=4, column=0, padx=(20, 0), pady=(0, 10))
        self.entry_vehicle_type = tk.Entry(self.output_frame, width=30)
        self.entry_vehicle_type.grid(row=4, column=1, padx=(0, 20), pady=(0, 10))
        self.entry_vehicle_type.config(state="readonly")
        self.entry_vehicle_desc = tk.Entry(self.output_frame, width=30)

        self.label_vehicle_desc = tk.Label(self.output_frame, text="Vehicle Description:", font=("Arial", 12), bg="light blue")
        self.label_vehicle_desc.grid(row=5, column=0, padx=(20, 0), pady=(0, 10))
        self.entry_vehicle_desc = tk.Entry(self.output_frame, width=30)
        self.entry_vehicle_desc.grid(row=5, column=1, padx=(0, 20), pady=(0, 10))
        self.entry_vehicle_desc.config(state="readonly")



        self.button_get_fee = tk.Button(self.output_frame, text="Get Fee", font=("Arial", 12), command=self.get_fee)
        self.button_get_fee.grid(row=6, column=0, columnspan=2, padx=(20, 0), pady=(0, 10))

        self.label_vehicle_parked = tk.Label(self.output_frame, text="Vehicle Currently Parked?:", font=("Arial", 12), bg="light blue")
        self.label_vehicle_parked.grid(row=0, column=2, padx=(20, 0), pady=(0, 10))

        self.entry_vehicle_parked = tk.Entry(self.output_frame, width=30)
        self.entry_vehicle_parked.grid(row=0, column=3, padx=(0, 20), pady=(0, 10))

        self.label_vehicle_slot = tk.Label(self.output_frame, text="Vehicle Slot:", font=("Arial", 12), bg="light blue")
        self.label_vehicle_slot.grid(row=1, column=2, padx=(20, 0), pady=(0, 10))

        self.entry_vehicle_slot = tk.Entry(self.output_frame, width=30)
        self.entry_vehicle_slot.grid(row=1, column=3, padx=(20, 0), pady=(0, 10))

        self.label_vehicle_area = tk.Label(self.output_frame, text="Vehicle Area:", font=("Arial", 12), bg="light blue")
        self.label_vehicle_area.grid(row=2, column=2, padx=(20, 0), pady=(0, 10))

        self.entry_vehicle_area = tk.Entry(self.output_frame, width=30)
        self.entry_vehicle_area.grid(row=2, column=3, padx=(0, 20), pady=(0, 10))


        # Create back button
        back_button = tk.Button(view_car_window, text="Back", font=("Arial", 12), command=lambda: [view_car_window.destroy(), self.master.deiconify()])
        back_button.pack(pady=10)

        # TODO: Add code for view car window

    def park_vehicle(self):
        # TODO: Add code for park vehicle
        license_plate = self.entry_license_plate.get()
        owner_info = self.entry_owner_info.get()
        parking_id = cursor.var(int)
        slot_val = cursor.var(int)
        slot_area = cursor.var(str)
        sa = ''

        try:
            cursor.callproc("PV_ON_LP", [license_plate, owner_info, parking_id, slot_val])
            self.entry_parking_id.config(state="normal")
            self.entry_parking_id.delete(0, tk.END)
            self.entry_parking_id.insert(0, parking_id.getvalue())
            cursor.execute("SELECT slotarea FROM parking_slot WHERE slotno = 1")
            result = cursor.fetchone()
            if result:
                sa = result[0]
            else:
                sa = ""
            if slot_val.getvalue() is not None:
                messagebox.showinfo("Vehicle Parked", f"PRINT RECEIPT: Your Vehicle is succesfully parked. \n Parking ID :{parking_id.getvalue()} Please head to Slot Area {sa}, Slot No: {slot_val.getvalue()}")
            


        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Error", str(e))
    
    def park_vehicle_lp(self, license_plate):
        license_plate = license_plate
        parking_id = cursor.var(int)
        slot_val = cursor.var(int)
        sa = ''
        try:
            cursor.callproc("PV_ON_LP", [license_plate, "", parking_id, slot_val])
            cursor.execute("SELECT slotarea FROM parking_slot WHERE slotno = 1")
            result = cursor.fetchone()
            if result:
                sa = result[0]
            else:
                sa = ""
            messagebox.showinfo("Vehicle Parked", f"PRINT RECEIPT: Your Vehicle is succesfully parked. \nParking ID: {parking_id.getvalue()} \nPlease head to Slot Area {sa}, Slot No: {slot_val.getvalue()}")
        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Error", str(e))

    def unpark_vehicle(self):
        # TODO: Add code for unpark vehicle
        
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
        if self.entry_parking_id.get() is not None:
               parking_id = self.entry_parking_id.get()
        license_plate = cursor.var(str)
        vehicle_name = cursor.var(str)
        vehicle_company = cursor.var(str)
        vehicle_type = cursor.var(str)
        vehicle_desc = cursor.var(str)
        fee = cursor.var(int)
        vehicle_slot = cursor.var(int)
        vehicle_area = cursor.var(str)

        try:
            cursor.callproc("ViewCar", [parking_id, license_plate, vehicle_name, vehicle_company, vehicle_type, vehicle_desc, fee])
            self.entry_license_plate.config(state="normal")
            self.entry_license_plate.delete(0, tk.END)
            try:
                
                self.entry_license_plate.insert(0, license_plate.getvalue() if license_plate is not None else "")
            except AttributeError:
                license_plate = ""
                self.entry_license_plate.insert(0,  "")
            
            self.entry_license_plate.config(state="readonly")

            self.entry_vehicle_name.config(state="normal")
            self.entry_vehicle_name.delete(0, tk.END)
            self.entry_vehicle_name.insert(0, vehicle_name.getvalue() if vehicle_name.getvalue() is not None else "")
            self.entry_vehicle_name.config(state="readonly")

            self.entry_vehicle_company.config(state="normal")
            self.entry_vehicle_company.delete(0, tk.END)
            self.entry_vehicle_company.insert(0, vehicle_company.getvalue() if vehicle_company.getvalue() is not None else "")
            self.entry_vehicle_company.config(state="readonly")
            
            self.entry_vehicle_type.config(state="normal")
            self.entry_vehicle_type.delete(0, tk.END)
            self.entry_vehicle_type.insert(0, vehicle_type.getvalue() if vehicle_type.getvalue() is not None else "")
            self.entry_vehicle_type.config(state="readonly")

            self.entry_vehicle_desc.config(state="normal")
            self.entry_vehicle_desc.delete(0, tk.END)
            self.entry_vehicle_desc.insert(0, vehicle_desc.getvalue() if vehicle_desc.getvalue() is not None else "")
            self.entry_vehicle_desc.config(state="readonly")

            self.entry_fee.config(state="normal")
            self.entry_fee.delete(0, tk.END)
            self.entry_fee.insert(0, fee.getvalue() if fee.getvalue() is not None else "")
            self.entry_fee.config(state="readonly")


            #find vehicle_slot and vehicle_area when parked is true USING VIEWSLOTPL FUNCTION
            try:
                cursor.callproc("ViewSlotPL", [license_plate.getvalue(), vehicle_slot, vehicle_area])
                self.entry_vehicle_slot.config(state="normal")
                self.entry_vehicle_slot.delete(0, tk.END)
                self.entry_vehicle_slot.insert(0, vehicle_slot.getvalue() if vehicle_slot.getvalue() is not None else "")
                self.entry_vehicle_slot.config(state="readonly")

                self.entry_vehicle_parked.config(state="normal")
                self.entry_vehicle_parked.delete(0, tk.END)
                self.entry_vehicle_parked.insert(0, "Yes")
                self.entry_vehicle_parked.config(state="readonly")


                self.entry_vehicle_area.config(state="normal")
                self.entry_vehicle_area.delete(0, tk.END)
                self.entry_vehicle_area.insert(0, vehicle_area.getvalue() if vehicle_area.getvalue() is not None else "")
                self.entry_vehicle_area.config(state="readonly")
            except cx_Oracle.DatabaseError as e: # if vehicle is not parked
                self.entry_vehicle_slot.config(state="normal")
                self.entry_vehicle_slot.delete(0, tk.END)
                self.entry_vehicle_slot.insert(0, 'N/A')
                self.entry_vehicle_slot.config(state="readonly")

                self.entry_vehicle_parked.config(state="normal")
                self.entry_vehicle_parked.delete(0, tk.END)
                self.entry_vehicle_parked.insert(0, "No")
                self.entry_vehicle_parked.config(state="readonly")

                self.entry_vehicle_area.config(state="normal")
                self.entry_vehicle_area.delete(0, tk.END)
                self.entry_vehicle_area.insert(0, 'N/A')
                self.entry_vehicle_area.config(state="readonly")


        except cx_Oracle.DatabaseError as e:
            messagebox.showerror("Error", str(e))
    
    def slot_viewer():
        pass
    
    

# Create main window
root = tk.Tk()
# Calculate the width and height of the window
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = int(screen_width * 0.75)
window_height = int(screen_height * 0.75)

# Calculate the x and y coordinates to center the window
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

# Set the window size and position
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

app = ParkingSystem(root)
root.mainloop()

# Close connection
cursor.close()
db.close()