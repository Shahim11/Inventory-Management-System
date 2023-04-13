from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
# pip install pillow || pip uninstall pillow || python --version || pip3.10 install Pillow

class supplierClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System | Developed By Shahim")
        self.root.config(bg="white")
        self.root.focus_force()

        # ==All Variables==
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_sup_invoice = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_contact = StringVar()

        # ==Search Frame==
        # SearchFrame = LabelFrame(self.root, text="Search Supplier", font=(
        #     "goudy old style", 12, "bold"), bd=2, relief=RIDGE, bg="white")
        # SearchFrame.place(x=250, y=20, width=600, height=70)

        # ==Options==
        lbl_search = Label(self.root, text="Invoice No. ",
                           font=("goudy old style", 15), bg="white")
        lbl_search.place(x=550, y=80)

        # ==Search Text==
        txt_search = Entry(self.root, textvariable=self.var_searchtxt, font=(
            "goudy old style", 15), bg="lightyellow").place(x=660, y=80, width=200)

        # ==Search Button==
        btn_search = Button(self.root, text="Search", command=self.search, font=(
            "goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2").place(x=875, y=77, width=120, height=30)

        # ==Title==
        title = Label(self.root, text="Supplier Details", font=("goudy old style", 20,
                      "bold"), bg="#0f4d7d", fg="white").place(x=50, y=10, width=1000, height=40)

        # ==Content==
        # ==Row 1==
        lbl_supplier_invoice = Label(self.root, text="Invoice No.", font=(
            "goudy old style", 15), bg="white").place(x=50, y=80)

        txt_supplier_invoice = Entry(self.root, textvariable=self.var_sup_invoice, font=(
            "goudy old style", 15), bg="lightyellow").place(x=180, y=80, width=180)

        # ==Row 2==
        lbl_name = Label(self.root, text="Name", font=(
            "goudy old style", 15), bg="white").place(x=50, y=120)

        txt_name = Entry(self.root, textvariable=self.var_name, font=(
            "goudy old style", 15), bg="lightyellow").place(x=180, y=120, width=180)

        # ==Row 3==
        lbl_contact = Label(self.root, text="Contact", font=(
            "goudy old style", 15), bg="white").place(x=50, y=160)

        txt_contact = Entry(self.root, textvariable=self.var_contact, font=(
            "goudy old style", 15), bg="lightyellow").place(x=180, y=160, width=180)

        # ==Row 4==
        lbl_email = Label(self.root, text="Email", font=(
            "goudy old style", 15), bg="white").place(x=50, y=200)

        txt_email = Entry(self.root, textvariable=self.var_email, font=(
            "goudy old style", 15), bg="lightyellow").place(
            x=180, y=200, width=180)

        # ==Row 5==
        lbl_address = Label(self.root, text="Address", font=(
            "goudy old style", 15), bg="white").place(x=50, y=240)

        self.txt_address = Text(self.root, font=(
            "goudy old style", 15), bg="lightyellow")
        self.txt_address.place(x=180, y=240, width=300, height=70)

        # ==Row 6==
        lbl_description = Label(self.root, text="Description", font=(
            "goudy old style", 15), bg="white").place(x=50, y=330)
        self.txt_description = Text(self.root, font=(
            "goudy old style", 15), bg="lightyellow")
        self.txt_description.place(x=180, y=330, width=300, height=70)

        # ==Buttons==
        btn_add = Button(self.root, text="Save", command=self.add, bg="#2196f3", font=(
            "oudy old style", 15), fg="white", cursor="hand2").place(x=55, y=440, width=90, height=35)

        btn_update = Button(self.root, text="Update", command=self.update, bg="#4caf50", font=(
            "oudy old style", 15), fg="white", cursor="hand2").place(x=165, y=440, width=90, height=35)

        btn_delete = Button(self.root, text="Delete", command=self.delete, bg="#f44336", font=(
            "oudy old style", 15), fg="white", cursor="hand2").place(x=275, y=440, width=90, height=35)

        btn_clear = Button(self.root, text="Clear", command=self.clear, bg="#607d8b", font=(
            "oudy old style", 15), fg="white", cursor="hand2").place(x=385, y=440, width=90, height=35)

        # ==Supplier Details==
        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=550, y=120, width=500, height=370)

        # scrollbar with treeview
        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.supplierTable = ttk.Treeview(emp_frame, columns=(
            "invoice", "name", "contact", "email", "address", "description"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)

        # heading and column set
        self.supplierTable.heading("invoice", text="Invoice No.")
        self.supplierTable.heading("name", text="Name")
        self.supplierTable.heading("contact", text="Contact")
        self.supplierTable.heading("email", text="Email")
        self.supplierTable.heading("address", text="Address")
        self.supplierTable.heading("description", text="Description")

        self.supplierTable["show"] = "headings"

        self.supplierTable.column("invoice", width=90)
        self.supplierTable.column("name", width=100)
        self.supplierTable.column("contact", width=100)
        self.supplierTable.column("email", width=100)
        self.supplierTable.column("address", width=100)
        self.supplierTable.column("description", width=100)

        self.supplierTable.pack(fill=BOTH, expand=1)
        self.supplierTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()

# ======================================
    def add(self):
        con = sqlite3.connect(database="ims.db")
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror(
                    "Error", "Invoice No Must be Required!", parent=self.root)
            else:
                cur.execute("select * from supplier where invoice=?",
                            (self.var_sup_invoice.get(), ))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror(
                        "Error", "This Invoice No is already assigned, try different one.")
                else:
                    cur.execute("Insert into supplier(invoice, name, contact,email, address, description) values(?,?,?,?,?,?)",
                                (
                                    self.var_sup_invoice.get(),
                                    self.var_name.get(),
                                    self.var_contact.get(),
                                    self.var_email.get(),
                                    self.txt_address.get('1.0', END),
                                    self.txt_description.get('1.0', END)
                                ))
                    con.commit()
                    messagebox.showinfo(
                        "Success", "Supplier Added Successfully.", parent=self.root)
                    self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

    def show(self):
        con = sqlite3.connect(database="ims.db")
        cur = con.cursor()
        try:
            cur.execute("select * from supplier")
            rows = cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                self.supplierTable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to : {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.supplierTable.focus()
        content = (self.supplierTable.item(f))
        row = content['values']
        print(row)
        self.var_sup_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.var_email.set(row[3])
        self.txt_address.delete('1.0', END)
        self.txt_address.insert(END, row[4])
        self.txt_description.delete('1.0', END)
        self.txt_description.insert(END, row[5])

    def update(self):
        con = sqlite3.connect(database="ims.db")
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice No. is empty!")
            else:
                cur.execute("Select * from supplier where invoice=?",
                            (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Error", "Invalid Invoice No.", parent=self.root)
                else:
                    cur.execute("update supplier set name=?,contact=?, email=?, address=?, description=? where invoice=?", (
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.var_email.get(),
                        self.txt_address.get('1.0', END),
                        self.txt_description.get('1.0', END),
                        self.var_sup_invoice.get(),
                    ))
                    con.commit()
                    messagebox.showinfo(
                        "Success", "Supplier Updated Successfully!")
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

    def delete(self):
        con = sqlite3.connect(database="ims.db")
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror(
                    "Error", "Invoice No. is Required!", parent=self.root)
            else:
                cur.execute("select * from supplier where invoice=?",
                            (self.var_sup_invoice.get(), ))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Error", "Invalid Invoice No.", parent=self.root)
                else:
                    op = messagebox.askyesno(
                        "Confirm", "Do you really want to delete?", parent=self.root)
                    if op == True:
                        cur.execute("delete from supplier where invoice=?",
                                    (self.var_sup_invoice.get(), ))
                        con.commit()
                        messagebox.showinfo(
                            "Success", "Supplier Deleted Successfully", parent=self.root)
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.var_email.set("")
        self.txt_address.delete('1.0', END)
        self.txt_description.delete('1.0', END)
        self.var_searchtxt.set("")
        self.show()

    def search(self):
        con = sqlite3.connect(database="ims.db")
        cur = con.cursor()
        try:
            if self.var_searchtxt.get() == "":
                messagebox.showerror(
                    "Error", "Invoice No. Should be Required!", parent=self.root)
            else:
                cur.execute("select * from supplier where invoice=?",
                            (self.var_searchtxt.get(), ))
                row = cur.fetchone()
                if row != None:
                    self.supplierTable.delete(
                        *self.supplierTable.get_children())
                    self.supplierTable.insert('', END, values=row)
                else:
                    messagebox.showerror(
                        "Error", "No Record Found.", parent=self.root)
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to : {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = supplierClass(root)
    root.mainloop()


# python Supplier.py
