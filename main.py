# Main file to connect all other .py files
import tkinter as tk
from app_gui import AppGui


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Stock Tracker")
window.config(padx=20, pady=20)

# Set the theme
window.tk.call("source", "azure.tcl")
window.tk.call("set_theme", "dark")

app = AppGui(window)
app.pack(fill="both", expand=True)

window.mainloop()
