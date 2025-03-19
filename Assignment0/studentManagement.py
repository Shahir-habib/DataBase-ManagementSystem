"""2. Consider list of departments (dept code and name), list of students (roll, dept code, 
name, address and phone) preloaded in array. Now develop an application for the 
following. 
User may add/search/edit/delete/display all student records. While adding, ensure roll 
must be unique, a list of dept name to be shown from which user selects one and 
corresponding dept code to be stored. On collecting the data user may choose 
CANCEL/SAVE button to decide course of action. For searching user provides roll. If it 
exists details are shown else suitable message to be displayed. To delete user provides 
roll. If it does not exist then suitable message is to be displayed. To edit also user 
provides roll. If it exists user may be allowed to edit any field except roll.  User may 
select CANCEL/SAVE to decide course of action. To display all records, at a time five 
records are to be shown. IT will also have PREV/NEXT button to display previous set 
and next set respectively. When first set is displayed PREV button must be disabled and 
at last set NEXT button must be disabled."""

import json
import tkinter as tk
from tkinter import messagebox, simpledialog

with open("records.json", "r") as fd:
    data = json.load(fd)

university_name = data["university"]
departments = data["departments"]
students = data["students"]

def save_data():
    """Save the updated student data back to the JSON file."""
    data["students"] = students
    with open("records.json", "w") as fd:
        json.dump(data, fd, indent=4)

def is_roll_unique(roll):
    return roll not in [student["roll"] for student in students]

def get_dept_code(dept_name):
    for dept in departments:
        if dept["name"] == dept_name:
            return dept["code"]
    return None

def add_student():
    def save():
        roll = roll_entry.get()
        name = name_entry.get()
        dept_name = dept_var.get()
        if not roll or not name or not dept_name:
            messagebox.showwarning("Input Error", "All fields are required!")
            return
        if not is_roll_unique(roll):
            messagebox.showwarning("Input Error", "Roll number must be unique!")
            return
        dept_code = get_dept_code(dept_name)
        if not dept_code:
            messagebox.showwarning("Input Error", "Invalid department selected!")
            return
        students.append({"roll": roll, "name": name, "dept": dept_code})
        save_data()
        messagebox.showinfo("Success", "Student added successfully!")
        add_window.destroy()

    def cancel():
        add_window.destroy()

    add_window = tk.Toplevel(root)
    add_window.title("Add Student")

    tk.Label(add_window, text="Roll Number:").grid(row=0, column=0, padx=10, pady=5)
    roll_entry = tk.Entry(add_window)
    roll_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Name:").grid(row=1, column=0, padx=10, pady=5)
    name_entry = tk.Entry(add_window)
    name_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(add_window, text="Department:").grid(row=2, column=0, padx=10, pady=5)
    dept_var = tk.StringVar(add_window)
    dept_var.set(departments[0]["name"])  # Default value
    dept_menu = tk.OptionMenu(add_window, dept_var, *[dept["name"] for dept in departments])
    dept_menu.grid(row=2, column=1, padx=10, pady=5)

    tk.Button(add_window, text="Save", command=save).grid(row=3, column=0, padx=10, pady=10)
    tk.Button(add_window, text="Cancel", command=cancel).grid(row=3, column=1, padx=10, pady=10)

def search_student():
    roll = simpledialog.askstring("Search Student", "Enter Roll Number:")
    if roll:
        for student in students:
            if student["roll"] == roll:
                messagebox.showinfo("Student Found", f"Name: {student['name']}\nDepartment: {student['dept']}")
                return
        messagebox.showinfo("Not Found", "Student with this roll number does not exist.")

def edit_student():
    roll = simpledialog.askstring("Edit Student", "Enter Roll Number:")
    if roll:
        for student in students:
            if student["roll"] == roll:
                def save():
                    student["name"] = name_entry.get()
                    student["dept"] = get_dept_code(dept_var.get())
                    save_data()
                    messagebox.showinfo("Success", "Student updated successfully!")
                    edit_window.destroy()

                def cancel():
                    edit_window.destroy()

                edit_window = tk.Toplevel(root)
                edit_window.title("Edit Student")

                tk.Label(edit_window, text="Name:").grid(row=0, column=0, padx=10, pady=5)
                name_entry = tk.Entry(edit_window)
                name_entry.insert(0, student["name"])
                name_entry.grid(row=0, column=1, padx=10, pady=5)

                tk.Label(edit_window, text="Department:").grid(row=1, column=0, padx=10, pady=5)
                dept_var = tk.StringVar(edit_window)
                dept_var.set([dept["name"] for dept in departments if dept["code"] == student["dept"]][0])
                dept_menu = tk.OptionMenu(edit_window, dept_var, *[dept["name"] for dept in departments])
                dept_menu.grid(row=1, column=1, padx=10, pady=5)

                tk.Button(edit_window, text="Save", command=save).grid(row=2, column=0, padx=10, pady=10)
                tk.Button(edit_window, text="Cancel", command=cancel).grid(row=2, column=1, padx=10, pady=10)
                return
        messagebox.showinfo("Not Found", "Student with this roll number does not exist.")

def delete_student():
    roll = simpledialog.askstring("Delete Student", "Enter Roll Number:")
    if roll:
        for student in students:
            if student["roll"] == roll:
                students.remove(student)
                save_data()
                messagebox.showinfo("Success", "Student deleted successfully!")
                return
        messagebox.showinfo("Not Found", "Student with this roll number does not exist.")

def display_students():
    """Display student records with pagination."""
    def update_display(start_index):
        # Clear the display text
        display_text.delete(1.0, tk.END)
        
        # Display the current set of records
        for i in range(start_index, min(start_index + 5, len(students))):
            student = students[i]
            display_text.insert(tk.END, f"Roll: {student['roll']}, Name: {student['name']}, Dept: {student['dept']}\n")
        
        # Update button states
        prev_button.config(state=tk.NORMAL if start_index > 0 else tk.DISABLED)
        next_button.config(state=tk.NORMAL if start_index + 5 < len(students) else tk.DISABLED)
        
        # Update the current start index
        nonlocal current_start_index
        current_start_index = start_index

    # Create a new window for displaying students
    display_window = tk.Toplevel(root)
    display_window.title("Display Students")

    # Text widget to display student records
    display_text = tk.Text(display_window, wrap=tk.NONE, width=50, height=10)
    display_text.pack(padx=10, pady=10)

    # Frame for navigation buttons
    button_frame = tk.Frame(display_window)
    button_frame.pack(pady=5)

    # Initialize the starting index
    current_start_index = 0

    # Previous and Next buttons
    prev_button = tk.Button(button_frame, text="Prev", command=lambda: update_display(current_start_index - 5))
    prev_button.pack(side=tk.LEFT, padx=5)
    next_button = tk.Button(button_frame, text="Next", command=lambda: update_display(current_start_index + 5))
    next_button.pack(side=tk.LEFT, padx=5)

    # Display the first set of records
    update_display(current_start_index)

root = tk.Tk()
root.title(f"{university_name} Student Management System")
root.geometry("600x800")
tk.Button(root, text="Add Student", command=add_student).pack(pady=5)
tk.Button(root, text="Search Student", command=search_student).pack(pady=5)
tk.Button(root, text="Edit Student", command=edit_student).pack(pady=5)
tk.Button(root, text="Delete Student", command=delete_student).pack(pady=5)
tk.Button(root, text="Display Students", command=display_students).pack(pady=5)

root.mainloop()