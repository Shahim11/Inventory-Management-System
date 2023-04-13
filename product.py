from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
# pip install pillow || pip uninstall pillow || python --version || pip3.10 install Pillow

class productClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System | Developed By Shahim")
        self.root.config(bg="white")
        self.root.focus_force()

        # ==All Variables==
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_pid = StringVar()
        self.var_category = StringVar()
        self.var_supplier = StringVar()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_quantity = StringVar()
        self.var_status = StringVar()

        self.category_list = []
        self.supplier_list = []
        self.fetch_supplier_category()

        # ==Product Details Manage Frame==
        product_frame = Frame(self.root, bd=3, relief=RIDGE, bg="white")
        product_frame.place(x=10, y=10, width=450, height=480)

        # ==Title==
        title = Label(product_frame, text="Manage Product Details", font=(
            "goudy old style", 18), bg="#0f4d7d", fg="white").pack(side=TOP, fill=X)

        # ==Content==
        # ==Column 1==
        lbl_category = Label(product_frame, text="Category", font=(
            "goudy old style", 18), bg="white").place(x=30, y=60)

        lbl_supplier = Label(product_frame, text="Supplier", font=(
            "goudy old style", 18), bg="white").place(x=30, y=110)

        lbl_name = Label(product_frame, text="Name", font=(
            "goudy old style", 18), bg="white").place(x=30, y=160)

        lbl_price = Label(product_frame, text="Price", font=(
            "goudy old style", 18), bg="white").place(x=30, y=210)

        lbl_quantity = Label(product_frame, text="Quantity", font=(
            "goudy old style", 18), bg="white").place(x=30, y=260)

        lbl_status = Label(product_frame, text="Status", font=(
            "goudy old style", 18), bg="white").place(x=30, y=310)

        # ==Column 2==
        cmb_category = ttk.Combobox(product_frame, textvariable=self.var_category, values=self.category_list,
                                    state="readonly", justify=CENTER, font=("goudy old style", 15))
        cmb_category.place(x=150, y=60, width=200)
        cmb_category.current(0)

        cmb_supplier = ttk.Combobox(product_frame, textvariable=self.var_supplier, values=self.supplier_list,
                                    state="readonly", justify=CENTER, font=("goudy old style", 15))
        cmb_supplier.place(x=150, y=110, width=200)
        cmb_supplier.current(0)

        txt_name = Entry(product_frame, textvariable=self.var_name, font=(
            "goudy old style", 15), bg="lightyellow").place(x=150, y=160, width=200)

        txt_price = Entry(product_frame, textvariable=self.var_price, font=(
            "goudy old style", 15), bg="lightyellow").place(x=150, y=210, width=200)

        txt_quantity = Entry(product_frame, textvariable=self.var_quantity, font=(
            "goudy old style", 15), bg="lightyellow").place(x=150, y=260, width=200)

        cmb_status = ttk.Combobox(product_frame, textvariable=self.var_status, values=(
            "Active", "Inactive"), state="readonly", justify=CENTER, font=("goudy old style", 15))
        cmb_status.place(x=150, y=310, width=200)
        cmb_status.current(0)

        # ==Buttons==
        btn_add = Button(product_frame, text="Save", command=self.add, font=(
            "oudy old style", 15), bg="#2196f3", fg="white", cursor='hand2').place(x=10, y=400, width=100, height=40)

        btn_update = Button(product_frame, text="Update", command=self.update, font=(
            "oudy old style", 15), bg="#4caf50", fg="white", cursor='hand2').place(x=120, y=400, width=100, height=40)

        btn_delete = Button(product_frame, text="Delete", font=("oudy old style", 15), command=self.delete,
                            bg="#f44336", fg="white", cursor='hand2').place(x=230, y=400, width=100, height=40)

        btn_clear = Button(product_frame, text="Clear", command=self.clear, font=(
            "oudy old style", 15), bg="#607f8b", fg="white", cursor='hand2').place(x=340, y=400, width=100, height=40)

        # ==Search Frame==
        searchFrame = LabelFrame(self.root, text="Search Product", bg="white", font=(
            "goudy old style", 12, "bold"), bd=2, relief=RIDGE)
        searchFrame.place(x=480, y=10, width=600, height=70)

        # ==Options==
        cmb_search = ttk.Combobox(searchFrame, textvariable=self.var_searchby, values=(
            "Select", "Category", "Supplier", "Name"), state="readonly", justify=CENTER, font=("goudy old style", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        # ==Search Text==
        txt_search = Entry(searchFrame, textvariable=self.var_searchtxt, font=(
            "goudy old style", 15), bg="lightyellow").place(x=200, y=10)

        # ==Search Button==
        btn_search = Button(searchFrame, text="Search", command=self.search, font=(
            "goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2").place(x=410, y=9, width=150, height=30)

        # ==Product Details==
        product_details_frame = Frame(self.root, bd=3, relief=RIDGE)
        product_details_frame.place(x=480, y=100, width=600, height=390)

        # scrollbar with treeview
        scrolly = Scrollbar(product_details_frame, orient=VERTICAL)
        scrollx = Scrollbar(product_details_frame, orient=HORIZONTAL)

        self.ProductTable = ttk.Treeview(product_details_frame, columns=(
            "pid", "category", "supplier", "name", "price", "quantity", "status"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.ProductTable.yview)
        scrollx.config(command=self.ProductTable.xview)

        # heading and column set
        self.ProductTable.heading("pid", text="P ID")
        self.ProductTable.heading("category", text="Category")
        self.ProductTable.heading("supplier", text="Supplier")
        self.ProductTable.heading("name", text="Name")
        self.ProductTable.heading("price", text="Price")
        self.ProductTable.heading("quantity", text="Qty")
        self.ProductTable.heading("status", text="Status")

        self.ProductTable["show"] = "headings"

        self.ProductTable.column("pid", width=90)
        self.ProductTable.column("category", width=100)
        self.ProductTable.column("supplier", width=100)
        self.ProductTable.column("name", width=100)
        self.ProductTable.column("price", width=100)
        self.ProductTable.column("quantity", width=100)
        self.ProductTable.column("status", width=100)

        self.ProductTable.pack(fill=BOTH, expand=1)
        self.ProductTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

# ======================================
    def fetch_supplier_category(self):
        con = sqlite3.connect(database="ims.db")
        cur = con.cursor()
        try:
            cur.execute("select name from category")
            category = cur.fetchall()
            self.category_list.append("Empty")
            if len(category) > 0:
                del self.category_list[:]
                self.category_list.append("Select")
                for i in category:
                    self.category_list.append(i[0])

            cur.execute("Select name from supplier")
            supplier = cur.fetchall()
            self.supplier_list.append("Empty")
            if len(supplier) > 0:
                del self.supplier_list[:]
                self.supplier_list.append("Select")
                for i in supplier:
                    self.supplier_list.append(i[0])
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to : {str(ex)}", parent=self.root)

    def add(self):
        con = sqlite3.connect(database="ims.db")
        cur = con.cursor()
        try:
            if self.var_category.get() == "Select" or self.var_category.get() == "Empty" or self.var_supplier.get() == "Select" or self.var_name.get() == "":
                messagebox.showerror(
                    "Error", "All fields are Required!", parent=self.root)
            else:
                cur.execute("select * from product where name=?",
                            (self.var_name.get(), ))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror(
                        "Error", "Product already present, try different one.")
                else:
                    cur.execute("Insert into product(category, supplier, name, price, quantity, status) values(?,?,?,?,?,?)",
                                (
                                    self.var_category.get(),
                                    self.var_supplier.get(),
                                    self.var_name.get(),
                                    self.var_price.get(),
                                    self.var_quantity.get(),
                                    self.var_status.get(),
                                ))
                    con.commit()
                    messagebox.showinfo(
                        "Success", "Product Added Successfully.", parent=self.root)
                    self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

    def show(self):
        con = sqlite3.connect(database="ims.db")
        cur = con.cursor()
        try:
            cur.execute("select * from product")
            rows = cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to : {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.ProductTable.focus()
        content = (self.ProductTable.item(f))
        row = content['values']
        print(row)
        self.var_pid.set(row[0])
        self.var_category.set(row[1])
        self.var_supplier.set(row[2])
        self.var_name.set(row[3])
        self.var_price.set(row[4])
        self.var_quantity.set(row[5])
        self.var_status.set(row[6])

    def update(self):
        con = sqlite3.connect(database="ims.db")
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Select product from list!!")
            else:
                cur.execute("Select * from product where pid=?",
                            (self.var_pid.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Error", "Invalid Product", parent=self.root)
                else:
                    cur.execute("update product set category=?, supplier=?, name=?, price=?, quantity=?, status=? where pid=?", (
                        self.var_category.get(),
                        self.var_supplier.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_quantity.get(),
                        self.var_status.get(),
                        self.var_pid.get(),
                    ))
                    con.commit()
                    messagebox.showinfo(
                        "Success", "Product Updated Successfully!")
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

    def delete(self):
        con = sqlite3.connect(database="ims.db")
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror(
                    "Error", "Product Id is Required!", parent=self.root)
            else:
                op = messagebox.askyesno(
                    "Confirm", "Do you really want to delete?", parent=self.root)
                if op == True:
                    cur.execute("delete from product where pid=?",
                                (self.var_pid.get(), ))
                    con.commit()
                    messagebox.showinfo(
                        "Success", "Product Deleted Successfully", parent=self.root)
                    self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

    def clear(self):
        self.var_pid.set("")
        self.var_name.set("")
        self.var_category.set("Select")
        self.var_supplier.set("Select")
        self.var_quantity.set("")
        self.var_price.set("")
        self.var_status.set("Active")
        self.show()

    def search(self):
        con = sqlite3.connect(database="ims.db")
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror(
                    "Error", "Select Search by Option!", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror(
                    "Error", "Search Input Should be Required!", parent=self.root)
            else:
                cur.execute("select * from product where " +
                            self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No Record Found.")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")


if __name__ == '__main__':
    root = Tk()
    obj = productClass(root)
    root.mainloop()


# python product.py
