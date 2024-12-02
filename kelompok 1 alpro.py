import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import random

# Data kutipan motivasi
motivational_quotes = [
    "Kata-kata hari ini.",
]

# Fungsi untuk menampilkan kutipan motivasi dengan jendela kustom
def show_motivational_quote():
    quote = random.choice(motivational_quotes)
    
    # Membuat jendela kustom
    quote_window = tk.Toplevel(root)
    quote_window.title("Motivational Quote")
    
    # Mengatur warna latar belakang dan ukuran jendela
    quote_window.geometry("400x200")
    quote_window.configure(bg='lightblue')
    
    # Menambahkan label untuk menampilkan kutipan
    quote_label = tk.Label(quote_window, text=quote, wraplength=350, bg='lightblue', font=("Comic Sans MS", 14))
    quote_label.pack(pady=20)

    # Menambahkan tombol untuk menutup jendela
    close_button = ttk.Button(quote_window, text="Close", command=quote_window.destroy)
    close_button.pack(pady=10)

# Fungsi Timer Belajar
def start_timer():
    try:
        minutes = int(timer_entry.get())
        seconds = minutes * 60
        countdown(seconds)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number of minutes.")

def countdown(t):
    while t > 0:
        mins, secs = divmod(t, 60)
        timer_var.set(f"{mins:02}:{secs:02}")
        time.sleep(1)
        t -= 1
    timer_var.set("Time's up!")
    messagebox.showinfo("Timer", "Time's up!")

def start_timer_thread():
    timer_thread = threading.Thread(target=start_timer)
    timer_thread.start()

# Fungsi Catatan Harian
def save_notes():
    notes = notes_text.get("1.0", tk.END)
    with open("notes.txt", "w") as file:
        file.write(notes)

def load_notes():
    try:
        with open("notes.txt", "r") as file:
            notes = file.read()
            notes_text.delete("1.0", tk.END)
            notes_text.insert(tk.END, notes)
    except FileNotFoundError:
        messagebox.showerror("File Not Found", "No notes found.")

# Fungsi To-Do List
def add_task():
    task = task_entry.get()
    if task:
        task_listbox.insert(tk.END, task)
        task_entry.delete(0, tk.END)

def mark_done():
    try:
        selected_task_index = task_listbox.curselection()[0]
        task_listbox.itemconfig(selected_task_index, {'bg':'lightgray'})  # Ubah warna latar
        task_listbox.selection_clear(selected_task_index)  # Hapus pemilihan
    except IndexError:
        messagebox.showwarning("No Selection", "Please select a task to mark as done.")

def delete_task():
    try:
        selected_task_index = task_listbox.curselection()[0]
        task_listbox.delete(selected_task_index)
    except IndexError:
        messagebox.showwarning("No Selection", "Please select a task to delete.")

def delete_all_tasks():
    task_listbox.delete(0, tk.END)

# Fungsi Kalkulator
def calc_button_click(char):
    current = calc_var.get()
    if char == "=":
        try:
            result = eval(current)
            calc_var.set(result)
        except Exception:
            calc_var.set("Error")
    elif char == "C":
        calc_var.set("")
    else:
        calc_var.set(current + char)

# Jendela Utama
root = tk.Tk()
root.title("Student Productivity Toolkit")
root.geometry("800x600")

# Menu Navigasi
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Menu untuk fitur
feature_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Features", menu=feature_menu)
feature_menu.add_command(label="Show Motivational Quote", command=show_motivational_quote)

# Tab Control
tab_control = ttk.Notebook(root)

# Timer Tab
timer_tab = ttk.Frame(tab_control, style='My.TFrame')
tab_control.add(timer_tab, text='Timer')

timer_var = tk.StringVar()
timer_label = ttk.Label(timer_tab, textvariable=timer_var, font=("Arial", 48))
timer_label.pack(pady=20)
timer_entry = ttk.Entry(timer_tab, font=("Arial", 16))
timer_entry.pack(pady=10)
start_button = ttk.Button(timer_tab, text="Start Timer", command=start_timer_thread)
start_button.pack(pady=10)

# Notes Tab
notes_tab = ttk.Frame(tab_control)
tab_control.add(notes_tab, text='Daily Notes')
notes_text = tk.Text(notes_tab, wrap='word', font=("Arial", 12))
notes_text.pack(pady=20, padx=20)
save_button = ttk.Button(notes_tab, text="Save Notes", command=save_notes)
save_button.pack(pady=5)
load_button = ttk.Button(notes_tab, text="Load Notes", command=load_notes)
load_button.pack(pady=5)

# To-Do List Tab
todo_tab = ttk.Frame(tab_control)
tab_control.add(todo_tab, text='To-Do List')
task_entry = ttk.Entry(todo_tab, font=("Arial", 16))
task_entry.pack(pady=10)
add_task_button = ttk.Button(todo_tab, text="Add Task", command=add_task)
add_task_button.pack(pady=5)
task_listbox = tk.Listbox(todo_tab, font=("Arial", 12))
task_listbox.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
done_button = ttk.Button(todo_tab, text="Mark Done", command=mark_done)
done_button.pack(pady=5)
delete_button = ttk.Button(todo_tab, text="Delete Task", command=delete_task)
delete_button.pack(pady=5)
delete_all_button = ttk.Button(todo_tab, text="Delete All Tasks", command=delete_all_tasks)
delete_all_button.pack(pady=5)

# Calculator Tab
calc_tab = ttk.Frame(tab_control)
tab_control.add(calc_tab, text='Calculator')
calc_var = tk.StringVar()
calc_entry = ttk.Entry(calc_tab, textvariable=calc_var, font=("Arial", 16), justify="right")
calc_entry.grid(row=0, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)

calc_buttons = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['0', '.', '=', '+'],
    ['C', None, None, None]
]

for r, row in enumerate(calc_buttons, start=1):
    for c, char in enumerate(row):
        if char:
            button = ttk.Button(calc_tab, text=char, command=lambda ch=char: calc_button_click(ch))
            button.grid(row=r, column=c, sticky='nsew', padx=2, pady=2)

for i in range(4):
    calc_tab.grid_columnconfigure(i, weight=1)
for i in range(len(calc_buttons) + 1):  # +1 for input row
    calc_tab.grid_rowconfigure(i, weight=1)

# Add tab control to main window
tab_control.pack(expand=1, fill='both')

# Run application
root.mainloop()