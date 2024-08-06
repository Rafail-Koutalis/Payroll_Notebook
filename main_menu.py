import center_window
import database
import tkinter as tk
from sys import exit
import signup
import login


def main_menu() :
    root = tk.Tk()
    root.bind('<Escape>',center_window.bind_escape)
    root.resizable(False,False)
    header_label = tk.Label(root,text="\n   Επιλέξτε λειτουργία.\nΗ αλλιώς πιέστε 1.\n",bg='black',fg='white',font=('helvetica',15,'bold'))
    header_label_2 = tk.Label(root,text="\n  Επιλέξτε λειτουργία.\nΗ πιέστε 1 για εγγραφή,\n2 για σύνδεση.\n",bg='black',fg='white',font=('helvetica',15,'bold'))

    signup_button = tk.Button(root,text="Εγγραφή",font=('helvetica',16,'bold'),width=20,borderwidth=5,relief=tk.RAISED,command=lambda :signup.signup_menu(root))
    login_button = tk.Button(root,text="Σύνδεση",bg='green',fg='white',font=('helvetica',16,'bold'),width=20,borderwidth=5,relief=tk.RAISED,command=lambda :login.login_menu(root))
    exit_button = tk.Button(root,text="Έξοδος",bg='red',font=('helvetica',16,'bold'),width=20,borderwidth=5,relief=tk.RAISED,command=lambda :exit())


    list_id = database.get_all_id()

    if not list_id :
        header_label.grid(row=0)
        root.bind("1",lambda event : signup.signup_menu(root))
        center_window.root_config(root, 'black', 'Αρχικό μενού.', 275, 230)
        signup_button.grid(row=1)
        exit_button.grid(row=2)
    else :
        header_label_2.grid(row=0)
        root.bind("1",lambda event :login.login_menu(root))
        root.bind("2",lambda event :signup.signup_menu(root))
        center_window.root_config(root, 'black', 'Αρχικό μενού.', 275, 270)
        signup_button.grid(row=1)
        login_button.grid(row=2)
        exit_button.grid(row=3)
    root.mainloop()

main_menu()