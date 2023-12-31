import tkinter as tk
from tkinter import ttk
import sqlite3


# making a MainFrame class
class GeneralFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.Employee = DB()
        self.view_records()

    def init_main(self):
        # creating toolbar
        toolbar = tk.Frame(bg="#badbad", bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # adding an add icon
        self.add_img = tk.PhotoImage(file="./img/add.png")

        # adding an add button
        btn_add_employee = tk.Button(
            toolbar,
            bg="#5ba154",
            bd=0,
            image=self.add_img,
            command=self.open_child_frame
        )
        btn_add_employee.pack(side=tk.LEFT)

        # creating a treeview widget
        self.tree = ttk.Treeview(
            self, columns=("ID", "name", "tel", "email", "salary"), height=45, show="headings"
        )

        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("name", width=300, anchor=tk.CENTER)
        self.tree.column("tel", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=150, anchor=tk.CENTER)
        self.tree.column("salary", width=150, anchor=tk.CENTER)

        self.tree.heading("ID", text="ID")
        self.tree.heading("name", text="ФИО")
        self.tree.heading("tel", text="Телефон")
        self.tree.heading("email", text="E-mail")
        self.tree.heading("salary", text="Зарплата")

        self.tree.pack(side=tk.LEFT)

        # adding an update icon
        self.update_img = tk.PhotoImage(file="./img/update.png")

        # adding an edit button
        btn_edit_employee = tk.Button(
            toolbar,
            bg="#5ba154",
            bd=0,
            image=self.update_img,
            command=self.open_update_dialog
        )
        btn_edit_employee.pack(side=tk.LEFT)

        # adding a delete icon
        self.delete_img = tk.PhotoImage(file="./img/delete.png")

        # adding a delete button
        btn_delete = tk.Button(
            toolbar,
            bg="#5ba154",
            bd=0,
            image=self.delete_img,
            command=self.delete_records
        )
        btn_delete.pack(side=tk.LEFT)

        # adding a search icon
        self.search_img = tk.PhotoImage(file="./img/search.png")

        # adding a search button
        btn_search = tk.Button(
            toolbar,
            bg="#5ba154",
            bd=0,
            image=self.search_img,
            command=self.open_search_dialog,
        )
        btn_search.pack(side=tk.LEFT)

    # creating a function for open dialog
    def open_child_frame(self):
        ChildFrame()

    # making a records function
    def records(self, name, tel, email, salary):
        self.Employee.insert_data(name, tel, email, salary)
        self.view_records()

    # making a function for print all from database
    def view_records(self):
        self.Employee.cursor.execute("SELECT * FROM Employee")
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row) for row in self.Employee.cursor.fetchall()]

    def open_update_dialog(self):
        Updating()

    # making a function for update data in database
    def update_records(self, name, tel, email, salary):
        self.Employee.cursor.execute(
            """UPDATE Employee SET name=?, tel=?, email=?, salary=? WHERE id=?""",
            (name, tel, email, salary, self.tree.set(self.tree.selection()[0], "#1")),
        )
        self.Employee.conn.commit()
        self.view_records()

    # making a function for delete data in database
    def delete_records(self):
        for selection_items in self.tree.selection():
            self.Employee.cursor.execute(
                "DELETE FROM Employee WHERE id=?", (self.tree.set(selection_items, "#1"))
            )
        self.Employee.conn.commit()
        self.view_records()

    def open_search_dialog(self):
        Finder()

    # making a function for search data in database
    def search_records(self, name):
        name = "%" + name + "%"
        self.Employee.cursor.execute("SELECT * FROM Employee WHERE name LIKE ?",
                                     (name,))

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row) for row in self.Employee.cursor.fetchall()]


# creating a child class
class ChildFrame(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    # initialization Child
    def init_child(self):
        self.title("Добавить")
        self.geometry("400x220")
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        # creating a labels
        label_name = tk.Label(self, text="ФИО:")
        label_name.place(x=50, y=50)
        label_select = tk.Label(self, text="Телефон:")
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text="E-mail:")
        label_sum.place(x=50, y=110)
        label_salary = tk.Label(self, text='Зарплата:')
        label_salary.place(x=50, y=140)

        # creating an entries
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80)
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=110)
        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=140)

        # adding a cancel button
        self.btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        self.btn_cancel.place(x=220, y=170)

        # adding a add button
        self.btn_ok = ttk.Button(self, text="Добавить")
        self.btn_ok.place(x=300, y=170)

        self.btn_ok.bind(
            "<Button-1>",
            lambda event: self.view.records(
                self.entry_name.get(), self.entry_email.get(), self.entry_tel.get(), self.entry_salary.get()
            ),
        )


# creating class for Updating
class Updating(ChildFrame):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.Employee = DB()
        self.default_data()

    # initialization Updating
    def init_edit(self):
        self.title("Редактирование контакта")
        btn_edit = ttk.Button(self, text="Редактировать")
        btn_edit.place(x=205, y=170)
        btn_edit.bind(
            "<Button-1>",
            lambda event: self.view.update_records(
                self.entry_name.get(), self.entry_email.get(), self.entry_tel.get(), self.entry_salary.get()
            ),
        )
        btn_edit.bind("<Button-1>", lambda event: self.destroy(), add="+")
        self.btn_ok.destroy()

    def default_data(self):
        self.Employee.cursor.execute(
            "SELECT * FROM Employee WHERE id=?",
            self.view.tree.set(self.view.tree.selection()[0], "#1"),
        )
        row = self.Employee.cursor.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_tel.insert(0, row[3])
        self.entry_salary.insert(0, row[4])


# creating a class for finding
class Finder(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    # initialization Search
    def init_search(self):
        self.title("Поиск контакта")
        self.geometry("300x100")
        self.resizable(False, False)

        label_search = tk.Label(self, text="Имя:")
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=100, y=20, width=150)

        # creating a cancel button
        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=185, y=50)

        # creating a search button
        search_btn = ttk.Button(self, text="Найти")
        search_btn.place(x=105, y=50)
        search_btn.bind(
            "<Button-1>",
            lambda event: self.view.search_records(self.entry_search.get()),
        )
        search_btn.bind("<Button-1>", lambda event: self.destroy(), add="+")


# creating DataBase class
class DB:
    def __init__(self):
        self.conn = sqlite3.connect("Company.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS Employee (
                id INTEGER PRIMARY KEY,
                name TEXT,
                tel TEXT,
                email TEXT,
                salary INTEGER
            )"""
        )
        self.conn.commit()

    # making a function for inserting data to database
    def insert_data(self, name, tel, email, salary):
        self.cursor.execute(
            """INSERT INTO Employee(name, tel, email, salary) VALUES(?, ?, ?, ?)""", (name, tel, email, salary)
        )
        self.conn.commit()


# running a app
if __name__ == "__main__":
    root = tk.Tk()
    employee = DB()
    app = GeneralFrame(root)
    app.pack()
    root.title("Список сотрудников компании")
    root.geometry("800x600")
    root['bg'] = '#badbad'
    root.resizable(False, False)
    root.mainloop()
