from tkinter import messagebox
import center_window
import database
import tkinter as tk
from sys import exit
from datetime import date
from tkinter import ttk

def show_specific_data(id,button) :
    user = database.get_specific_user_view(id)
    root = tk.Tk()
    root.resizable(False,False)
    root.bind('<Escape>',lambda event:root.destroy())
    center_window.root_config(root, 'white', f"Δεδομένα {id} ", 485, 128)
    # define columns

    tree_columns = ('Μηνιαίες ώρες', 'Μηνιαίος μισθός', 'Συνολικός μισθός')
    tree = ttk.Treeview(root, columns=tree_columns, show='headings',height=5)
    style = ttk.Style()
    style.configure("Treeview",rowheight=50, font=('helvetica', 13), background='white', foreground='black', fieldground='white')
    style.configure("Treeview.Heading", font=('Helvetica', 12), foreground='black')
    for column in tree_columns:
        tree.heading(column, text=column)
        tree.column(column, anchor='center', width=160)

    # define headings
    tree.insert('',tk.END,values=user)

    tree.grid(row=1, column=0, sticky='nsew')
    # run the app
    root.mainloop()

def show_all_data() :
    users_data = database.get_all_users_view()
    root = tk.Tk()
    root.bind('<Escape>',lambda event:root.destroy())
    root.resizable(False,False)
    center_window.root_config(root,'white',"Δεδομένα χρηστών",580,428)
    style = ttk.Style()
    style.configure("Treeview",font=('helvetica',9),background='white',foreground='black',fieldground='white')

    # define columns
    tree_columns = ('Χρήστης', 'Μηνιαίες ώρες', 'Μηνιαίος μισθός','Συνολικός μισθός')

    tree = ttk.Treeview(root, columns=tree_columns, show='headings',height=20)
    for column in tree_columns :
        tree.heading(column,text=column)
        tree.column(column,anchor='center',width=140)

    tree.tag_configure('oddrow', background='lightgray')
    tree.tag_configure('evenrow', background='white')

    index = 4
    for user in users_data:
        row_tag = 'oddrow' if index % 2 == 0 else 'evenrow'
        tree.insert('',tk.END, values=user,tags=(row_tag,))
        index-=1

    tree.grid(row=1, column=0, sticky='nsew')

    # add a scrollbar
    scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=1, column=1, sticky='ns')

    # run the app
    root.mainloop()




def check_hours_entry(id,hours_entry,hours_entry_2,button_save) :
    if hours_entry_2.get() != "" and hours_entry.get()!="" :
        try:

            if hours_entry_2.get() != hours_entry.get() :
                center_window.entry_clear(hours_entry,hours_entry_2,entry_1=hours_entry)
                messagebox.showerror("Σφάλμα","Οι δύο εισαγωγές ωρών εργασίας διαφέρουν!\nΠαρακαλώ ξαναεισάγετε τες.")

            elif float(hours_entry.get()) > 9 or float(hours_entry_2.get()) > 9:
                center_window.entry_clear(hours_entry, hours_entry_2, entry_1=hours_entry)
                messagebox.showerror("Σφάλμα", "Οι ώρες εργασίας δεν μπορούν να ξεπερνούν τις 9!")
            else :
                # try :
                    entry_mistakes = len(hours_entry.get())
                    print(entry_mistakes)
                    while entry_mistakes != 0 :
                        for character in hours_entry.get() :
                            if character == "," or character == "." :
                                entry_mistakes-=1
                                continue
                            elif (not character.isnumeric()) :
                                    center_window.entry_clear(hours_entry,hours_entry_2,entry_1=hours_entry)
                                    hours_entry.focus()
                                    messagebox.showerror("Σφάλμα","Επιτρέπονται μόνο αριθμοί,κόμματα,και τελείες.")
                            else :
                                entry_mistakes -= 1
                    hours_to_save = float(hours_entry.get())
                    result = messagebox.askyesno("Confirmation", f"Εισαγάγατε ώρες : {hours_entry.get()}.\nΘέλετε να προχωρήσετε?")
                    if result:
                        database.update_user_data(id, hours_to_save, str(date.today())[8:])
                        hours_entry.config(state='disabled')
                        hours_entry_2.config(state='disabled')
                        button_save.config(state='disabled')
                        messagebox.showinfo("Επιτυχία", "Οι σημερινές ώρες εργασίας αποθηκεύτηκαν με επιτυχία.\n"
                                                        "Πιέστε έξοδο ή επιστροφή.")
                    else:
                        center_window.entry_clear(hours_entry,hours_entry_2,entry_1=hours_entry)
                        messagebox.showinfo("Επιστροφή","Επαναεισάγετε τις ώρες εργασίας")
        except:
            center_window.entry_clear(hours_entry, hours_entry_2,entry_1=hours_entry)
            messagebox.showerror("Σφάλμα", "Έγινε μη αποδεκτή εισαγωγή ωρών..\nΠαρακαλώ ξαναεισάγετε τις ώρες.")
    else:
        center_window.entry_clear(hours_entry, hours_entry_2, entry_1=hours_entry)
        messagebox.showerror("Σφάλμα", "Συμπληρώστε και τα δύο πεδία.")

def update_hours_menu(id,root,hours_button) :

    today_date = str(date.today())[8:]
    this_month = str(date.today())[5:7]
    user_last_worked_date = database.get_user_date(id)
    user_month_in_database = database.get_user_month(id)
    if this_month != user_month_in_database :
        database.reset_total_month_pay(id)
    if today_date == user_last_worked_date:
        messagebox.showerror("Σφάλμα", "Δεν μπορείτε να ξαναεισάγετε ώρες εργασίας για σήμερα.\nΜπορείτε μόνο να δείτε τα δεδομένα σας έως αύριο,\nή να πραγματοποιήσετε έξοδο.")
        hours_button.config(state='disabled')
    else :

        root.destroy()
        new_root = tk.Tk()
        new_root.resizable(False,False)
        new_root.lift()
        new_root.focus_force()
        new_root.bind('<Escape>',lambda event :exit())
        new_root.bind('<Return>',lambda event:check_hours_entry(id,hours_entry,hours_entry_2,button_save))
        center_window.root_config(new_root, 'black', "Αποθήκευση ωρών εργασίας", 300, 390)

        header_label = tk.Label(new_root,text="\n  Εισάγετε τις σημερινές \nώρες εργασίας.",font=('helvetica',14,'bold'),bg='black',fg='white')
        hours_entry = tk.Entry(new_root,font=('helvetica',15,'bold'),width=21,borderwidth=5,relief=tk.RAISED)
        hours_entry.focus()
        label_reenter_hours = tk.Label(new_root,text="  Επιβεβαιώστε τις \nώρες εργασίας.",font=('helvetica',15,'bold'),bg='black',fg='white')
        hours_entry_2 = tk.Entry(new_root,font=('helvetica',15,'bold'),width=21,borderwidth=5,relief=tk.RAISED)

        button_save = tk.Button(new_root,text="Αποθήκευση",font=('helvetica',16,'bold'),
                                bg='green',fg='white',width=22,borderwidth=5,relief=tk.RAISED,command=lambda :check_hours_entry(id,hours_entry,hours_entry_2,button_save))
        button_return = tk.Button(new_root,text="Επιστροφή",font=('helvetica',16,'bold'),width=22,borderwidth=5,relief=tk.RAISED,command=lambda :main_functions(id,new_root))

        empty_label_1 = tk.Label(new_root, text="",bg='black')
        empty_label_2 = tk.Label(new_root, text="", bg='black')
        exit_button = tk.Button(new_root, text="Έξοδος", width=22, borderwidth=5,
                                font=('helvetica', 16, 'bold'),bg='red',fg='white', relief=tk.RAISED, command=lambda: exit())

        header_label.grid(row=0)
        hours_entry.grid(row=1)
        empty_label_1.grid(row=2)
        label_reenter_hours.grid(row=3)
        hours_entry_2.grid(row=4)
        empty_label_2.grid(row=5)
        button_save.grid(row=6)
        button_return.grid(row=7)
        exit_button.grid(row=8)

def main_functions(id,old_root) :
    old_root.destroy()
    user_role = database.get_user_role(id)
    new_root = tk.Tk()
    new_root.bind('<Escape>',lambda event :exit())
    new_root.resizable(False,False)


    header_label = tk.Label(new_root,text="  Επιλέξτε μία από τις λειτουργίες.\n\n",bg='black',fg='white',font=('helvetica',15,'bold'))
    empty_label = tk.Label(new_root,text="",bg='black')
    hours_update_button = tk.Button(new_root,text="Αποθήκευση ωρών εργασίας",width=24,borderwidth=5,font=('helvetica',15,'bold'),relief=tk.RAISED,command=lambda :update_hours_menu(id,new_root,hours_update_button))
    data_show_button_employer = tk.Button(new_root, text="Προβολή δεδομένων εργασίας", width=24, borderwidth=5,
                                    font=('helvetica', 15, 'bold'), relief=tk.RAISED, command=lambda: show_all_data())
    data_show_button_employee = tk.Button(new_root, text="Προβολή δεδομένων εργασίας", width=24, borderwidth=5,
                                          font=('helvetica', 15, 'bold'), relief=tk.RAISED,
                                          command=lambda: show_specific_data(id,data_show_button_employee))
    exit_button = tk.Button(new_root,bg='red',fg='white',text="Έξοδος",width=20, borderwidth=5,
                                    font=('helvetica', 15, 'bold'), relief=tk.RAISED, command=lambda: exit())


    if user_role == "Εργοδότης" :
        center_window.root_config(new_root,'black',f"Χρήστης {id}",330,210)
        header_label.grid(row=0)
        data_show_button_employer.grid(row=1)
        empty_label.grid(row=2)
    else :
        center_window.root_config(new_root, 'black', f"Χρήστης {id}", 330, 250)
        header_label.grid(row=0)
        hours_update_button.grid(row=1)
        data_show_button_employee.grid(row=2)
        empty_label.grid(row=3)

    exit_button.grid(row=4)
    new_root.mainloop()












