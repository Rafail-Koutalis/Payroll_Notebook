
from sys import exit
import center_window
import tkinter as tk
from tkinter import messagebox
import database
import after_signuplogin as after

def login_function(old_root,id_entry,password_entry,button_enter) :
    id = id_entry.get()
    password = password_entry.get()
    if (not id) or (not password) :
        center_window.entry_clear(id_entry,password_entry,entry_1=id_entry)
        messagebox.showerror("Σφάλμα","Παρακαλώ συμπληρώστε όλα τα πεδία.")
    elif database.login_authenticate(id,password) == 0 :
        center_window.entry_clear(id_entry, password_entry,entry_1=id_entry)
        messagebox.showerror("Σφάλμα","Τα στοιχεία που εισάγατε δεν αντιστοιχούν σε κάποιον χρήστη.")
    elif database.login_authenticate(id,password) == -1 :
        center_window.entry_clear(id_entry,password_entry,entry_1=id_entry)
        messagebox.showerror("Σφάλμα","Τα στοιχεία που εισάγατε είναι λανθασμένα.")
    else :
        center_window.entry_clear(id_entry,password_entry,entry_1=id_entry)
        id_entry.config(state='disabled')
        password_entry.config(state='disabled')
        button_enter.config(state='disabled')
        messagebox.showinfo("Επιτυχία","Τα στοιχεία σας ταυτοποιήθηκαν με επιτυχία!\nΘα ανακατευθυνθείτε μόλις κλείσετε το παράθυρο αυτό.")
        after.main_functions(id,old_root)



def login_menu(old_root) :
    root = tk.Tk()
    root.bind('<Escape>',lambda event :exit())
    root.bind('Return',lambda event :login_function(root,username_entry,password_entry,enter_button))
    root.resizable(False,False)
    old_root.destroy()
    center_window.root_config(root,'black','Mενού σύνδεσης',370,330)
    root.lift()
    root.focus_force()
    header_label = tk.Label(root,text="\nΕισάγετε τα στοιχεία σας στις φόρμες.\n",bg='black',fg='white',font=('helvetica',15,'bold'))
    empty_label = tk.Label(root,text='',bg='black')
    username_label = tk.Label(root,text="Όνομα χρήστη",bg='black',fg='white',font=('helvetica',15,'bold'))
    password_label = tk.Label(root,text="Κωδικός",bg='black',fg='white',font=('helvetica',15,'bold'))
    username_entry = tk.Entry(root,width=27,borderwidth=5,relief=tk.RAISED,font=('helvetica',15,'bold'))
    username_entry.focus()
    password_entry = tk.Entry(root, width=27,show='*', borderwidth=5, relief=tk.RAISED, font=('helvetica', 15, 'bold'))
    enter_button = tk.Button(root,text="Εισαγωγή",bg='green',fg='white',width=20,borderwidth=5,relief=tk.RAISED,font=('helvetica',15,'bold'),command=lambda :login_function(root,username_entry,password_entry,enter_button))
    root.bind('<Return>',lambda event:login_function(root,username_entry,password_entry,enter_button))
    exit_button = tk.Button(root,text="Έξοδος",bg='red',fg='white', width=20, borderwidth=5, relief=tk.RAISED, font=('helvetica', 15, 'bold'),
                            command=lambda: exit())
    header_label.grid(row=0)
    username_label.grid(row=1)
    username_entry.grid(row=2)
    password_label.grid(row=3)
    password_entry.grid(row=4)
    empty_label.grid(row=5)
    enter_button.grid(row=6)
    exit_button.grid(row=7)
    root.mainloop()
    