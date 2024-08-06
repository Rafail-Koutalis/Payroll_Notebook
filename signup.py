from tkinter import messagebox
from sys import exit
import center_window
import tkinter as tk
import database
import after_signuplogin as after
from datetime import date

def signup_func(root,id_entry,password_entry,hourly_rate_entry) :
    if not id_entry.get() or not password_entry.get() or not hourly_rate_entry.get() :
        center_window.entry_clear(id_entry,password_entry,hourly_rate_entry,entry_1=id_entry)
        id_entry.focus()
        messagebox.showerror("Σφάλμα","Πρέπει να συμπληρώσετε όλα τα πεδία")
    elif len(id_entry.get())<4 :
        center_window.entry_clear(id_entry, password_entry, hourly_rate_entry,entry_1=id_entry)
        id_entry.focus()
        messagebox.showerror("Σφάλμα", "Το όνομα χρήστη πρέπει να περιέχει 4 χαρακτήρες και πάνω.")
    elif len(password_entry.get())<4 :
        center_window.entry_clear(id_entry, password_entry, hourly_rate_entry,entry_1=id_entry)
        id_entry.focus()
        messagebox.showerror("Σφάλμα", "Ο κωδικός χρήστη πρέπει να περιέχει 4 χαρακτήρες και πάνω.")
    elif len(hourly_rate_entry.get())>3 :
        center_window.entry_clear(id_entry, password_entry, hourly_rate_entry,entry_1=id_entry)
        id_entry.focus()
        messagebox.showerror("Σφάλμα", "Η είσοδος ωρομισθίου πρέπει να περιέχει έως 3 xαρακτήρες.")
    else :
        list_id = database.get_all_id()
        id_found = 0
        if list_id :
            for key in list_id :
                if key[0] == id_entry.get() :
                    id_found += 1
        if id_found != 0 :
            center_window.entry_clear(id_entry,password_entry,hourly_rate_entry,entry_1=id_entry)
            id_entry.focus()
            messagebox.showerror("Σφάλμα","Το ID που επιλέξατε χρησιμοποιείτε ήδη.\nΕπιλέξτε κάποιο άλλο, αφού κλείσετε το παράθυρο.")
        else :
            today_month = str(date.today())[5:7]
            database.insert_new_member(id_entry.get(), password_entry.get(), hourly_rate_entry.get(), today_month)
            for widget in root.winfo_children() :
                widget.configure(state='disabled')
            messagebox.showinfo("Επιλογή ρόλου", "Παρακαλώ, επιλέξτε τον ρόλο σας στο κατάστημα.")
            id = id_entry.get()
            root.destroy()


            new_root = tk.Tk()
            center_window.root_config(new_root, 'black', "Επιλογή ρόλου", 420, 310)
            new_root.bind('<Escape>',lambda event:exit())

            employee_button = tk.Button(new_root, text="Υπάλληλος", font=('helvetica', 16, 'bold'), width=20, borderwidth=5,
                                        relief=tk.RAISED,
                                        command=lambda: role_choosing(new_root,id, "Υπάλληλος"))

            manager_button = tk.Button(new_root, text="Υπεύθυνος", font=('helvetica', 16, 'bold'), width=20, borderwidth=5,
                                       relief=tk.RAISED,
                                       command=lambda: role_choosing(new_root,id, "Υπεύθυνος"))

            boss_button = tk.Button(new_root, text="Αφεντικό", font=('helvetica', 16, 'bold'), width=20, borderwidth=5,
                                    relief=tk.RAISED,
                                    command=lambda: role_choosing(new_root,id, "Εργοδότης"))
            exit_button = tk.Button(new_root, text="Έξοδος", font=('helvetica', 16, 'bold'), width=20, borderwidth=5,
                                    relief=tk.RAISED, command=lambda: exit())
            empty_label = tk.Label(new_root,text="", bg='black')
            header_label = tk.Label(new_root,text="Επιλέξτε έναν από τους παρακάτω ρόλους.\n\n",font=('helvetica',15,'bold'),bg='black',fg='white')
            header_label.grid(row=0)
            employee_button.grid(row=1)
            manager_button.grid(row=2)
            boss_button.grid(row=3)
            empty_label.grid(row=4)
            exit_button.grid(row=5)

def role_choosing(root,user_id,role) :
    database.update_role(user_id,role)
    for widget in root.winfo_children() :
        if isinstance(widget,tk.Button) :
            widget.config(state='disabled')

    messagebox.showinfo("Εγγραφή επιτυχής","Τα στοιχεία σας αποθηκεύτηκαν με επιτυχία.\nΠιέστε 'ΟΚ' για να προχωρήσετε.")
    after.main_functions(user_id,root)


def signup_menu(old_root):
    database.create_table()
    old_root.destroy()
    root = tk.Tk()
    root.lift()
    root.focus_force()
    root.bind('<Escape>',lambda event :exit())
    root.bind('<Return>',lambda  event :signup_func(root,id_entry,password_entry,hourly_rate_entry) )
    root.resizable(False,False)
    center_window.root_config(root,'black','Μενού εγγραφής',280,400)


    header_label = tk.Label(root, text=" Συμπληρώστε όλα τα πεδία.\n\n", bg="black", fg='white',
                            font=('helvetica', 15, 'bold'))
    id_label = tk.Label(root, text="Κωδικός ID", bg='black', fg='white', font=('helvetica', 15, 'bold'))
    id_entry = tk.Entry(root, width=20, borderwidth=5,font=('helvetica',15,'bold'), relief=tk.SUNKEN)
    id_entry.focus()
    password_label = tk.Label(root, text="Κωδικός πρόσβασης", bg='black', fg='white', font=('helvetica', 15, 'bold'))
    password_entry = tk.Entry(root, width=20, borderwidth=5,font=('helvetica',15,'bold'), relief=tk.SUNKEN)
    hourly_rate_label = tk.Label(root, text="Ωρομίσθιο", bg='black', fg='white', font=('helvetica', 15, 'bold'))
    hourly_rate_entry = tk.Entry(root, width=20, borderwidth=5,font=('helvetica',15,'bold'), relief=tk.SUNKEN)
    empty_label = tk.Label(text="", bg='black')
    enter_button = tk.Button(root, text="Αποθήκευση", bg='green',fg='white',font=('helvetica', 16, 'bold'), width=20, borderwidth=5,
                             relief=tk.RAISED,
                             command=lambda: signup_func(root,id_entry,password_entry,hourly_rate_entry))
    exit_button = tk.Button(root, text="Έξοδος",bg='red',fg='white', font=('helvetica', 16, 'bold'), width=20, borderwidth=5,
                            relief=tk.RAISED, command=lambda: exit())


    header_label.grid(row=0)
    id_label.grid(row=1)
    id_entry.grid(row=2)
    password_label.grid(row=3)
    password_entry.grid(row=4)
    hourly_rate_label.grid(row=5)
    hourly_rate_entry.grid(row=6)
    empty_label.grid(row=7)
    enter_button.grid(row=8)
    exit_button.grid(row=9)
    root.mainloop()




