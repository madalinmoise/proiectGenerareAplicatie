# toast.py
import customtkinter as ctk

class Toast(ctk.CTkFrame):
    def __init__(self, master, message, color="#2e7d32", duration=3000):
        super().__init__(master, fg_color=color, corner_radius=10)
        
        self.label = ctk.CTkLabel(self, text=message, text_color="white", font=("Inter", 13, "bold"), padx=20, pady=10)
        self.label.pack()
        
        self.place(relx=0.5, rely=0.1, anchor="n")
        
        # Auto-destruct after duration
        self.after(duration, self.fade_out)
        
    def fade_out(self):
        # Simplistic "fade out" by destroying
        self.destroy()

def show_toast(master, message, type="success"):
    color = "#2e7d32" if type == "success" else "#c62828"
    if type == "info": color = "#0288d1"
    Toast(master, message, color=color)
