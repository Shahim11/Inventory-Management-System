from tkinter import *
from PIL import Image, ImageTk
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
from tkinter import ttk, messagebox
import sqlite3
import time
import os
import tempfile

# pip install pillow || pip uninstall pillow || python --version || pip3.10 install Pillow

class billClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1365x700+0+0")
        self.root.title("Inventory Management System | Developed By Shahim")
        self.root.config(bg="white")

        # ==All Variables==
        self.var_search = StringVar()
        self.var_customer_name = StringVar()
        self.var_contact = StringVar()
        self.cart_list = []
        self.check_print= 0

        # ==Title==
        self.icon_title = Image.open("./images/logo1.png")
        self.icon_title = self.icon_title.resize((60, 60), Image.Resampling.LANCZOS)
        self.icon_title = ImageTk.PhotoImage(self.icon_title)

        title = Label(self.root, text="Inventory Management System", image=self.icon_title, compound=LEFT, font=(
            "times new roman", 40, "bold"), bg="#010c48", fg="white", anchor="w", padx=20).place(x=0, y=0, relwidth=1, height=70)

        # ==Button Logout==
        btn_logout = Button(self.root, text="Logout", font=("times new roman", 15, "bold"),
                            bg="yellow", cursor="hand2").place(x=1150, y=10, height=50, width=150)
        
        # ==Clock==
        self.lbl_clock = Label(self.root, text="Welcome to Inventory Management System\t\tDate : DD-MM-YYYY\t\tTime : HH:MM:SS",
                               font=("times new roman", 15), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=70,  relwidth=1, height=30)

        # ==Product Frame==
        productFrame1 = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        productFrame1.place(x=6, y=110, width=410, height=550)

        product_title = Label(productFrame1, text="All Products", font=(
            "goudy old style", 20, "bold"), bg="#262626", fg="white").pack(side=TOP, fill=X)

        # ==Product Search Frame==
        productFrame2 = Frame(productFrame1, bd=4, relief=RIDGE, bg="white")
        productFrame2.place(x=6, y=42, width=394, height=90)

        lbl_search = Label(productFrame2, text="Search Product | By Name", font=(
            "times new roman", 15, "bold"), fg="green", bg="white").place(x=2, y=5)
        lbl_name = Label(productFrame2, text="Product Name", font=(
            "times new roman", 15, "bold"), bg="white").place(x=2, y=45)
        txt_search = Entry(productFrame2, textvariable=self.var_search, font=(
            "times new roman", 15), bg="lightyellow").place(x=130, y=48, width=150, height=22)
        
        btn_search = Button(productFrame2, text="Search", command=self.search, font=("goudy old style", 15),
                            bg="#2196f3", fg="white", cursor="hand2").place(x=285, y=45, width=100, height=25)
        btn_show = Button(productFrame2, text="Show All", command=self.show, font=("goudy old style", 15),
                          bg="#083531", fg="white", cursor="hand2").place(x=285, y=10, width=100, height=25)

        # ==Product Details Frame==
        productFrame3 = Frame(productFrame1, bd=3, relief=RIDGE)
        productFrame3.place(x=2, y=140, width=398, height=375)

        # scrollbar with treeview
        scrolly = Scrollbar(productFrame3, orient=VERTICAL)
        scrollx = Scrollbar(productFrame3, orient=HORIZONTAL)

        self.product_table = ttk.Treeview(productFrame3, columns=(
            "pid", "name", "price", "quantity", "status"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.product_table.yview)
        scrollx.config(command=self.product_table.xview)

        self.product_table.heading("pid", text="PID")
        self.product_table.heading("name", text="Name")
        self.product_table.heading("price", text="Price")
        self.product_table.heading("quantity", text="Qty")
        self.product_table.heading("status", text="Status")

        self.product_table["show"] = "headings"

        self.product_table.column("pid", width=50)
        self.product_table.column("name", width=120)
        self.product_table.column("price", width=60)
        self.product_table.column("quantity", width=50)
        self.product_table.column("status", width=70)

        self.product_table.pack(fill=BOTH, expand=1)
        self.product_table.bind("<ButtonRelease-1>", self.get_data)

        lbl_note = Label(productFrame1, text="Note : Enter 0 quantity to remove product from the Cart.", font=(
            "goudy old style", 12), bg="white", fg="red").pack(side=BOTTOM, fill=X)

        # ==Customer Frame==
        CustomerFrame=Frame(self.root, bd=3, relief=RIDGE, bg="white")
        CustomerFrame.place(x=420, y=110, width=530, height=70)

        customer_title = Label(CustomerFrame, text="Customer Details", font=(
            "goudy old style", 15), bg="lightgray").pack(side=TOP, fill=X)
        
        lbl_name = Label(CustomerFrame, text="Name", font=(
            "times new roman", 15), bg="white").place(x=5, y=35)
        txt_name = Entry(CustomerFrame, textvariable=self.var_customer_name, font=(
            "times new roman", 13), bg="lightyellow").place(x=80, y=35, width=180, height=22)

        lbl_contact = Label(CustomerFrame, text="Contact No.", font=(
            "times new roman", 15), bg="white").place(x=270, y=35)
        txt_contact = Entry(CustomerFrame, textvariable=self.var_contact, font=(
            "times new roman", 13), bg="lightyellow").place(x=380, y=35, width=140, height=22)

        # ==Calculator Cart Frame==
        cal_cart_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        cal_cart_Frame.place(x=420, y=190, width=530, height=360)
    
        # ==Calculator Frame==
        self.var_cal_input = StringVar()

        cal_Frame = Frame(cal_cart_Frame, bd=9, relief=RIDGE, bg="white")
        cal_Frame.place(x=5, y=10, width=268, height=340)
   
        self.txt_cal_input = Entry(cal_Frame, textvariable=self.var_cal_input, font=(
            "arial", 15, "bold"), width=21, bd=10, relief=GROOVE, state='readonly', justify=RIGHT)
        self.txt_cal_input.grid(row=0, columnspan=4)

        # ==Row 1==
        btn_7 = Button(cal_Frame, text='7', font=("arial", 15, "bold"), command=lambda: self.get_input(7), bd=5, width=4, pady=10, cursor="hand2").grid(
            row=1, column=0)
        
        btn_8 = Button(cal_Frame, text='8', font=("arial", 15, "bold"), command=lambda: self.get_input(8), bd=5, width=4, pady=10, cursor="hand2").grid(
            row=1, column=1)
        
        btn_9 = Button(cal_Frame, text='9', font=("arial", 15, "bold"), command=lambda: self.get_input(9), bd=5, width=4, pady=10, cursor="hand2").grid(
            row=1, column=2)
        
        btn_sum = Button(cal_Frame, text='+', font=("arial", 15, "bold"), command=lambda: self.get_input('+'), bd=5, width=4, pady=10, cursor="hand2").grid(
            row=1, column=3)

        # ==Row 2==
        btn_4 = Button(cal_Frame, text='4', font=("arial", 15, "bold"), command=lambda: self.get_input(4), bd=5, width=4, pady=10, cursor="hand2").grid(
            row=2, column=0)
        
        btn_5 = Button(cal_Frame, text='5', font=("arial", 15, "bold"), command=lambda: self.get_input(5), bd=5, width=4, pady=10, cursor="hand2").grid(
            row=2, column=1)
       
        btn_6 = Button(cal_Frame, text='6', font=("arial", 15, "bold"), command=lambda: self.get_input(6), bd=5, width=4, pady=10, cursor="hand2").grid(
            row=2, column=2)
        
        btn_sub = Button(cal_Frame, text='-', font=("arial", 15, "bold"), command=lambda: self.get_input('-'), bd=5, width=4, pady=10, cursor="hand2").grid(
            row=2, column=3)

        # ==Row 3==
        btn_1 = Button(cal_Frame, text='1', font=("arial", 15, "bold"), command=lambda: self.get_input(1), bd=5, width=4, pady=10, cursor="hand2").grid(
            row=3, column=0)
        
        btn_2 = Button(cal_Frame, text='2', font=("arial", 15, "bold"), command=lambda: self.get_input(2), bd=5, width=4, pady=10, cursor="hand2").grid(
            row=3, column=1)
        
        btn_3 = Button(cal_Frame, text='3', font=("arial", 15, "bold"), command=lambda: self.get_input(3), bd=5, width=4, pady=10, cursor="hand2").grid(
            row=3, column=2)
        
        btn_mul = Button(cal_Frame, text='x', font=("arial", 15, "bold"), command=lambda: self.get_input('*'), bd=5, width=4, pady=10, cursor="hand2").grid(
            row=3, column=3)

        # ==Row 4==
        btn_0 = Button(cal_Frame, text='0', font=("arial", 15, "bold"), command=lambda: self.get_input(0), bd=5, width=4, pady=15, cursor="hand2").grid(
            row=4, column=0)
        
        btn_c = Button(cal_Frame, text='c', font=("arial", 15, "bold"), command=self.clear_cal, bd=5, width=4, pady=15, cursor="hand2").grid(
            row=4, column=1)
        
        btn_eq = Button(cal_Frame, text='=', font=("arial", 15, "bold"), command=self.perform_cal, bd=5, width=4, pady=15, cursor="hand2").grid(
            row=4, column=2)
        
        btn_div = Button(cal_Frame, text='/', font=("arial", 15, "bold"), command=lambda: self.get_input('/'), bd=5, width=4, pady=15, cursor="hand2").grid(
            row=4, column=3)


        # ==Cart Frame==
        cart_Frame = Frame(cal_cart_Frame, bd=3, relief=RIDGE)
        cart_Frame.place(x=280, y=8, width=245, height=342)
        
        self.cartTitle = Label(cart_Frame, text="Cart \t Total Products : [0]", font=(
            "goudy old style", 15), bg="lightgray")
        self.cartTitle.pack(side=TOP, fill=X)

        # scrollbar with treeview
        scrolly = Scrollbar(cart_Frame, orient=VERTICAL)
        scrollx = Scrollbar(cart_Frame, orient=HORIZONTAL)

        self.cart_table = ttk.Treeview(cart_Frame, columns=(
            "pid", "name", "price", "quantity"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.cart_table.yview)
        scrollx.config(command=self.cart_table.xview)

        self.cart_table.heading("pid", text="PID")
        self.cart_table.heading("name", text="Name")
        self.cart_table.heading("price", text="Price")
        self.cart_table.heading("quantity", text="Qty")

        self.cart_table["show"] = "headings"

        self.cart_table.column("pid", width=40)
        self.cart_table.column("name", width=120)
        self.cart_table.column("price", width=60)
        self.cart_table.column("quantity", width=50)

        self.cart_table.pack(fill=BOTH, expand=1)
        self.cart_table.bind("<ButtonRelease-1>", self.get_data_cart)

        # ==Add Cart Widgets Frame==
        self.var_pid = StringVar()
        self.var_product_name = StringVar()
        self.var_price = StringVar()
        self.var_quantity = StringVar()
        self.var_stock = StringVar()

        add_cart_widgets_frame = Frame(
            self.root, bd=2, relief=RIDGE, bg="white")
        add_cart_widgets_frame.place(x=420, y=550, width=530, height=110)

        lbl_product_name = Label(add_cart_widgets_frame, text="Product Name", font=(
            "times new roman", 15), bg="white").place(x=5, y=5)
        txt_name = Entry(add_cart_widgets_frame, textvariable=self.var_product_name, font=(
            "times new roman", 15), bg="lightyellow", state="readonly").place(x=5, y=35, width=190, height=22)

        lbl_product_price = Label(add_cart_widgets_frame, text="Price Per Qty", font=(
            "times new roman", 15), bg="white").place(x=210, y=5)
        txt_price = Entry(add_cart_widgets_frame, textvariable=self.var_price, font=(
            "times new roman", 15), bg="lightyellow", state="readonly").place(x=210, y=35, width=150, height=22)

        lbl_product_quantity = Label(add_cart_widgets_frame, text="Quantity", font=(
            "times new roman", 15), bg="white").place(x=380, y=5)
        txt_quantity = Entry(add_cart_widgets_frame, textvariable=self.var_quantity, font=(
            "times new roman", 15), bg="lightyellow").place(x=380, y=35, width=130, height=22)
        
        self.lbl_instock = Label(add_cart_widgets_frame, text="In Stock [0]", font=(
            "times new roman", 15), bg="white")
        self.lbl_instock.place(x=5, y=70)

        # ==Buttons==
        btn_clear_cart = Button(add_cart_widgets_frame, command = self.clear_cart, text="Clear", font=(
            "times new roman", 15, "bold"), bg="lightgray", cursor="hand2").place(x=180, y=70, width=150, height=30)
              
        btn_add_cart = Button(add_cart_widgets_frame, command = self.add_update_cart, text="Add | Update Cart", font=(
            "times new roman", 15, "bold"), bg="orange", cursor="hand2").place(x=340, y=70, width=180, height=30)

        # ==Billing Area==
        billFrame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        billFrame.place(x=953, y=110, width=410, height=410)

        billTitle = Label(billFrame, text="Customer Bill Area", font=(
            "goudy old style", 20, "bold"), bg="#f44336", fg="white").pack(side=TOP, fill=X)
        scrolly = Scrollbar(billFrame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)

        self.txt_bill_area = Text(billFrame, yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        # ==Billing Buttons==
        billMenuFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        billMenuFrame.place(x=953, y=520, width=410, height=140)

        self.lbl_amount = Label(billMenuFrame, text="Bill Amount\n[0]", font=(
            "goudy old style", 15, "bold"), bg="#3f51b5", fg="white")
        self.lbl_amount.place(x=2, y=5, width=120, height=70)

        self.lbl_discount = Label(billMenuFrame, text="Discount\n[5%]", font=(
            "goudy old style", 15, "bold"), bg="#8bc34a", fg="white")
        self.lbl_discount.place(x=124, y=5, width=120, height=70)

        self.lbl_net_pay = Label(billMenuFrame, text="Net Pay\n[0]", font=(
            "goudy old style", 15, "bold"), bg="#607d8b", fg="white")
        self.lbl_net_pay.place(x=246, y=5, width=160, height=70)

        btn_print = Button(billMenuFrame, text="Print", command=self.print_bill, cursor="hand2", font=("goudy old style", 15, "bold"),
                           bg="lightgreen", fg="white")
        btn_print.place(x=2, y=80, width=120, height=50)

        btn_clear_all = Button(billMenuFrame, text="Clear All", command=self.clear_all, cursor="hand2", font=("goudy old style", 15, "bold"),
                               bg="gray", fg="white")
        btn_clear_all.place(x=124, y=80, width=120, height=50)

        btn_generate = Button(billMenuFrame, text="Generate/\nSave Bill", command=self.generate_bill, cursor="hand2", font=("goudy old style", 15, "bold"),
                              bg="#009688", fg="white")
        btn_generate.place(x=246, y=80, width=160, height=50)

        # ==Footer==
        footer = Label(self.root, text="IMS-Inventory Management System | Developed By Shahim\nFor any Technical Issue contact: +8801758687203",
                       font=("times new roman", 11), bg="#4d636d", fg="white").pack(side=BOTTOM, fill=X)

        self.show()
        self.update_date_time()
     
# ======================================
    # ==All Functions==

    def get_input(self, num):
        xnum = self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        result = self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

    # ==Product Details Show==
    def show(self):
        con = sqlite3.connect(database="ims.db")
        cur = con.cursor()
        try:
            cur.execute("select pid, name, price, quantity, status from product where status='Active'")
            rows = cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to : {str(ex)}", parent=self.root)
        
    # ==Product Search==
    def search(self):
        con = sqlite3.connect(database="ims.db")
        cur = con.cursor()
        try:
            if self.var_search.get() == "":
                messagebox.showerror(
                    "Error", "Search Input Should be Required!", parent=self.root)
            else:
                cur.execute("select pid, name, price, quantity, status from product where name LIKE '%"+self.var_search.get()+"%' and status='Active'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No Record Found.")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")   

    # ==Get Product Data==        
    def get_data(self, ev):
        f = self.product_table.focus()
        content = (self.product_table.item(f))
        row = content['values']
        self.var_pid.set(row[0]) 
        self.var_product_name.set(row[1]) 
        self.var_price.set(row[2])        
        self.lbl_instock.config(text=f"In Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_quantity.set('1')

    # ==Get Product Data for Cart==
    def get_data_cart(self, ev):
        f = self.cart_table.focus()
        content = (self.cart_table.item(f))
        row = content['values']
        self.var_pid.set(row[0])
        self.var_product_name.set(row[1])
        self.var_price.set(row[2])
        self.var_quantity.set(row[3])
        self.lbl_instock.config(text=f"In Stock [{str(row[4])}]")
        self.var_stock.set(row[4])

    # ==Add/Update Product Data to Cart== 
    def add_update_cart(self):
        if self.var_pid.get() == '':
            messagebox.showerror("Error", "Please select product from the list", parent=self.root)
        elif self.var_quantity.get() == '':
            messagebox.showerror("Error", "Quantity is Required!", parent=self.root)
        elif int(self.var_quantity.get()) > int(self.var_stock.get()):
            messagebox.showerror("Error", "Invalid Quantity", parent=self.root)
        else:
            price_cal = self.var_price.get()
            cart_data = [self.var_pid.get(), self.var_product_name.get(), price_cal, self.var_quantity.get(), self.var_stock.get()]

            # ==Update Cart Data ==
            present = 'no'
            index1 = 0
            for row in self.cart_list:
                if self.var_pid.get() == row[0]:
                    present = 'yes'
                    break
                index1 += 1
            if present == 'yes':
                op = messagebox.askyesno('Confirm', "Product already present\nDo you want to Update | Remove the Cart List", parent=self.root)
                if op == True:
                    if self.var_quantity.get() == "0":
                        self.cart_list.pop(index1)
                    else:
                        #self.cart_list[index1][2] = price_cal  # price
                        self.cart_list[index1][3] = self.var_quantity.get() # quantity
            else:
                self.cart_list.append(cart_data)
            
            self.show_cart()
            self.bill_updates()
            self.clear_cart()
    
    # ==Bill Details Update==
    def bill_updates(self):
        self.bill_amount = 0
        self.net_pay = 0
        self.discount= 0
        for row in self.cart_list:
            self.bill_amount= self.bill_amount + (float(row[2])*int(row[3]))

        self.discount = (self.bill_amount * 5) / 100
        self.net_pay = self.bill_amount-self.discount
        self.lbl_amount.config(text=f'Bill Amount(Tk)\n{str(self.bill_amount)}')
        self.lbl_net_pay.config(text=f'Net Pay(Tk)\n{str(self.net_pay)}')
        self.cartTitle.config(text=f"Cart \t Total Product: [{str(len(self.cart_list))}]")

    # ==Product Details Show to Cart==
    def show_cart(self):
        try:
            self.cart_table.delete(*self.cart_table.get_children())
            for row in self.cart_list:
                self.cart_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    # ==Bill Generate==
    def generate_bill(self):
        if self.var_customer_name.get()=='' or self.var_contact.get()=='':
            messagebox.showerror('Error',f"Customer Deatils are required!",parent=self.root)
        elif len(self.cart_list) == 0:
            messagebox.showerror("Error", f"Please Add Product to the Cart!", parent=self.root)
        else:
            self.bill_top()           
            self.bill_middle()            
            self.bill_bottom()
            self.bill_footer()

            fp = open(f'bills/{str(self.invoice)}.txt', 'w')
            fp.write(self.txt_bill_area.get('1.0', END))
            fp.close()
            messagebox.showinfo('Saved', "Bill has been Generated/Saved in Database.", parent=self.root)
            
            self.check_print = 1
    
    # ==Bill Top==
    def bill_top(self):
        self.invoice = int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top_temp = f'''
\t\tTraitstore-Inventory
\tPhone No. +8801712345678, Dhaka-1229
{str("="*47)}
 Customer Name: {self.var_customer_name.get()}
 Phone No.: {self.var_contact.get()}
 Bill No.: {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*47)}
 Product Name\t\t\tQty\tPrice
{str("="*47)} 
        '''
        self.txt_bill_area.delete('1.0', END)
        self.txt_bill_area.insert('1.0', bill_top_temp)

    # ==Bill Middle==
    def bill_middle(self):
        conn = sqlite3.connect(database=r'ims.db')
        cursor = conn.cursor()
        try:
            for row in self.cart_list:
                pid = row[0]
                name = row[1]
                quantity = int(row[4]) - int(row[3])
                if int(row[3]) == int(row[4]):
                    status = 'Inactive'
                if int(row[3]) != int(row[4]):
                    status = 'Active'
                price = float(row[2])*int(row[3])
                price = str(price)
                self.txt_bill_area.insert(END, "\n "+name+"\t\t\t"+row[3]+"\tTk."+price)
                # ==Update Quantity in Product Table==
                cursor.execute("UPDATE product SET quantity=?, status=? WHERE pid=?", (
                    quantity,
                    status,
                    pid
                ))
                conn.commit()
            conn.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    # ==Bill Bottom==
    def bill_bottom(self):
        bill_bottom_temp = f'''
{str("="*47)}
 Bill Amount:\t\t\t\tTk.{self.bill_amount}
 Discount:\t\t\t\tTk.{self.discount}
 Net Pay:\t\t\t\tTk.{self.net_pay}
{str("="*47)}
        '''
        self.txt_bill_area.insert(END, bill_bottom_temp)

    # ==Bill Footer==
    def bill_footer(self):
        # font=("goudy old style", 15, "bold")
        bill_footer_temp = f'''
 Note: Purchases of Defected Item Must be 
 Exchanged by 72 Hour with Invoice. 
                    (Condition Applicable)
 
 Thank You for Shopping at Traitstore & 
 Please Come again.
        '''
        self.txt_bill_area.insert(END, bill_footer_temp)

    # ==Clear Cart Details==
    def clear_cart(self):
        self.var_pid.set('')
        self.var_product_name.set('')
        self.var_price.set('')
        self.var_quantity.set('')
        self.lbl_instock.config(text=f"In Stock")
        self.var_stock.set('')

    # ==Clear All Details==
    def clear_all(self):
        del self.cart_list[:]
        self.var_customer_name.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0', END)
        self.cartTitle.config(text=f"Cart \t Total Product: [0]")
        self.var_search.set('')
        self.lbl_amount.config(text=f"Bill Amount\n[0]")
        self.lbl_discount.config(text=f"Discount\n[5%]")
        self.lbl_net_pay.config(text=f"Net Pay\n[0]")  
        self.clear_cart()
        self.show()
        self.show_cart()
        self.check_print = 0

    # ==Update Date & Time==
    def update_date_time(self):
        time1 = time.strftime("%I:%M:%S")
        date1 = time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date1)}\t\t Time: {str(time1)}")
        self.lbl_clock.after(200, self.update_date_time)

    # ==Bill Print==
    def print_bill(self):
        if self.check_print == 1:
            messagebox.showinfo('Print', "Pleasse wait while printing", parent=self.root)
            new_file = tempfile.mktemp('.txt')
            open(new_file, 'w').write(self.txt_bill_area.get('1.0', END))
            os.startfile(new_file, 'print')
        else:
            messagebox.showerror('Print', "Pleasse generate bill, to print the receipt", parent=self.root)

if __name__ == '__main__':
    root = Tk()
    obj = billClass(root)
    root.mainloop()


# python billing.py
