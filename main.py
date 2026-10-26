import tkinter as tk
from tkinter import messagebox
from dronekit import connect, VehicleMode
import threading


class GCSControlPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Drone GCS Control Panel")
        self.root.geometry("400x500")

        self.vehicle = None

        # --- Connection Section ---
        tk.Label(root, text="Connection String:", font=("Arial", 12, "bold")).pack(pady=5)
        self.conn_entry = tk.Entry(root, width=25, font=("Arial", 11))
        self.conn_entry.insert(0, "127.0.0.1:14550")
        self.conn_entry.pack(pady=5)

        self.btn_connect = tk.Button(root, text="Connect", bg="green", fg="white", font=("Arial", 11, "bold"), width=15,
                                     command=self.connect_drone)
        self.btn_connect.pack(pady=5)

        self.btn_disconnect = tk.Button(root, text="Disconnect", bg="red", fg="white", font=("Arial", 11, "bold"),
                                        width=15, state=tk.DISABLED, command=self.disconnect_drone)
        self.btn_disconnect.pack(pady=5)

        tk.Label(root, text="---------------------------------------------").pack(pady=5)

        # --- Arm / Disarm Section ---
        self.btn_arm = tk.Button(root, text="ARM Drone", bg="orange", font=("Arial", 11, "bold"), width=20,
                                 state=tk.DISABLED, command=lambda: self.set_arm(True))
        self.btn_arm.pack(pady=5)

        self.btn_disarm = tk.Button(root, text="DISARM Drone", bg="gray", font=("Arial", 10), width=20,
                                    state=tk.DISABLED, command=lambda: self.set_arm(False))
        self.btn_disarm.pack(pady=5)

        tk.Label(root, text="---------------------------------------------").pack(pady=5)

        # --- Flight Modes Section ---
        tk.Label(root, text="Flight Modes", font=("Arial", 12, "bold")).pack(pady=5)

        modes = ["GUIDED", "STABILIZE", "LOITER", "LAND", "RTL"]
        for mode in modes:
            b = tk.Button(root, text=mode, font=("Arial", 10), width=18, state=tk.DISABLED,
                          command=lambda m=mode: self.set_mode(m))
            b.pack(pady=2)
            # Save references to buttons to enable/disable them easily later
            setattr(self, f"btn_{mode.lower()}", b)

    def connect_drone(self):
        conn_str = self.conn_entry.get()
        try:
            messagebox.showinfo("Connecting", f"Connecting to {conn_str}...")
            # Using threading so the GUI doesn't freeze while connecting
            threading.Thread(target=self._threaded_connect, args=(conn_str,), daemon=True).start()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _threaded_connect(self, conn_str):
        try:
            self.vehicle = connect(conn_str, wait_ready=True, timeout=60)
            print("Connected successfully!")
            self.root.after(0, self.update_ui_connected)
        except Exception as e:
            print(f"Connection failed: {e}")
            self.root.after(0, lambda: messagebox.showerror("Connection Failed", str(e)))

    def update_ui_connected(self):
        self.btn_connect.config(state=tk.DISABLED)
        self.conn_entry.config(state=tk.DISABLED)
        self.btn_disconnect.config(state=tk.NORMAL)
        self.btn_arm.config(state=tk.NORMAL)
        self.btn_disarm.config(state=tk.NORMAL)

        modes = ["GUIDED", "STABILIZE", "LOITER", "LAND", "RTL"]
        for mode in modes:
            getattr(self, f"btn_{mode.lower()}").config(state=tk.NORMAL)

        messagebox.success = messagebox.showinfo("Success", "Successfully connected to Drone!")

    def disconnect_drone(self):
        if self.vehicle:
            self.vehicle.close()
            self.vehicle = None
        self.btn_connect.config(state=tk.NORMAL)
        self.conn_entry.config(state=tk.NORMAL)
        self.btn_disconnect.config(state=tk.DISABLED)
        self.btn_arm.config(state=tk.DISABLED)
        self.btn_disarm.config(state=tk.DISABLED)

        modes = ["GUIDED", "STABILIZE", "LOITER", "LAND", "RTL"]
        for mode in modes:
            getattr(self, f"btn_{mode.lower()}").config(state=tk.DISABLED)

        print("Disconnected.")

    def set_arm(self, arm_status):
        if self.vehicle:
            if arm_status:
                self.vehicle.armed = True
                print("Command sent: ARM")
            else:
                self.vehicle.armed = False
                print("Command sent: DISARM")

    def set_mode(self, mode_name):
        if self.vehicle:
            self.vehicle.mode = VehicleMode(mode_name)
            print(f"Flight mode changed to: {mode_name}")


if __name__ == "__main__":
    root = tk.Tk()
    app = GCSControlPanel(root)
    root.mainloop()