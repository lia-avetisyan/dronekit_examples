import tkinter as tk
from pymavlink import mavutil

vehicle = None

def connect_drone():
    global vehicle
    connection_string = entry_conn.get()
    try:
        vehicle = mavutil.mavlink_connection(connection_string)
        vehicle.wait_heartbeat()
        print("Connected!")
    except Exception as e:
        print("Connection failed:", e)

def close_connection():
    global vehicle
    if vehicle:
        vehicle.close()
        print("Connection closed")

def arm_drone():
    if vehicle:
        vehicle.arducopter_arm()
        print("Arming drone...")

def set_mode(mode_name):
    if vehicle:
        mode_id = vehicle.mode_mapping().get(mode_name)
        vehicle.set_mode(mode_id)
        print(f"Mode set to {mode_name}")

root = tk.Tk()
root.title("My Simple GCS")

tk.Label(root, text="Connection String:").pack()
entry_conn = tk.Entry(root, width=30)
entry_conn.insert(0, "udp:127.0.0.1:14550")
entry_conn.pack()

btn_connect = tk.Button(root, text="Connect", command=connect_drone)
btn_connect.pack()

btn_close = tk.Button(root, text="Close Connection", command=close_connection)
btn_close.pack()

btn_arm = tk.Button(root, text="ARM", command=arm_drone, bg="red", fg="white")
btn_arm.pack(pady=10)

tk.Label(root, text="Modes:").pack()
modes = ["GUIDED", "STABILIZE", "LOITER", "LAND", "RTL"]

for m in modes:
    btn = tk.Button(root, text=m, command=lambda mode=m: set_mode(mode))
    btn.pack()

root.mainloop()
