from tkinter import*
from tkinter import font
# pip install pillow || pip uninstall pillow || python --version || pip3.10 install Pillow
from PIL import Image,ImageTk
from tkinter import messagebox
import sqlite3
import os
import time
import email_pass
import smtplib      # pip install smtplib

class loginSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Login System | Developed By Shahim")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#fafafa")

        # ==All Variables==
        self.employee_id = StringVar()
        self.password = StringVar()
        self.otp = ''

        # ==Images==
        self.phone_image = ImageTk.PhotoImage(file="images/phone.png")
        self.lbl_phone_image = Label(self.root, image=self.phone_image,bd=0).place(x=200,y=50)

        # ==Login Frame==
        login_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        login_frame.place(x=650, y=90, width=350, height=460)

        # ==Title==
        title = Label(login_frame,text="Login System",font=("Elephant",30,"bold"), bg="white").place(x=0,y=30,relwidth=1)

        lbl_user = Label(login_frame,text="Employee ID",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=100)
        
        txt_employee_id = Entry(login_frame,textvariable=self.employee_id,font=("times new roman",15),bg="#ECECEC").place(x=50,y=140,width=250)

        lbl_pass = Label(login_frame, text="Password", font=("Andalus", 15), bg="white", fg="#767171").place(x=50,y=200)
        txt_pass = Entry(login_frame, textvariable=self.password,show="*", font=("times new roman", 15), bg="#ECECEC").place(x=50, y=240, width=250)

       # ==Buttons==
        btn_login = Button(login_frame, command=self.login, text="Log In", font=("Arial Rounded MT Bold",15),bg="#00B0F0",activebackground="#00B0F0",fg="white",activeforeground="white",cursor="hand2").place(x=50,y=300,width=250,height=35)

        hr = Label(login_frame, bg="lightgray").place(x=50, y=370, width= 250, height=2)
        or_ = Label(login_frame, text="OR", bg="white", fg="lightgray", font=("times new roman",15,"bold")).place(x=150,y=355)

        btn_forget=Button(login_frame, text="Forgot Password?", command=self.forget_password_window, font=("times new roman",13),bg="white",fg="#00759E",bd=0,activebackground="white",activeforeground="#00759E",cursor="hand2").place(x=110,y=390)

        # ==Frame 2==
        register_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        register_frame.place(x=650, y=570, width=350, height=60)

        lbl_reg = Label(register_frame, text="This Software is Created by Shahim ",font=("times new roman",15),bg="white").place(x=0,y=20,relwidth=1)

        # ==Animated Images==
        self.image1 = ImageTk.PhotoImage(file="images/img1.png")
        self.image2 = ImageTk.PhotoImage(file="images/img2.png")
        self.image3 = ImageTk.PhotoImage(file="images/img3.png")

        self.lbl_change_image = Label(self.root, bg="white")
        self.lbl_change_image.place(x=367,y=153,width=240,height=428)

        self.animate()

# ======================================
    def animate(self):
        self.image=self.image1
        self.image1=self.image2
        self.image2=self.image3
        self.image3=self.image
        self.lbl_change_image.config(image=self.image)
        self.lbl_change_image.after(2000,self.animate)

    def login(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.employee_id.get()=="" or self.password.get()=="":
                messagebox.showerror("Error!","All fields are required!",parent=self.root)
            else:
                cur.execute("select utype from employee where eid=? AND pass=? ",(self.employee_id.get(),self.password.get()))
                user = cur.fetchone()

                if user == None:
                    messagebox.showerror("Error!","Invalid USERNAME/PASSWORD",parent=self.root)

                else:
                    if user[0] == "Admin":
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")
                        
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def forget_password_window(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.employee_id.get()=="" :
                messagebox.showerror("Error","Employee ID is required!",parent=self.root)

            else:
                cur.execute("select email from employee where eid=?",(self.employee_id.get(),))
                email = cur.fetchone()

                if email == None:
                    messagebox.showerror("Error!","Invalid Employee ID",parent=self.root)

                else:
                    #==Forget Window==
                    self.var_otp = StringVar()
                    self.var_new_pass = StringVar()
                    self.var_conf_pass = StringVar()
                    #call send_email_function()
                    check = self.send_email(email[0])

                    if check != 'Success':
                        messagebox.showerror("Error!","Connection Error,Try Again!", parent=self.root)
                    else:
                        self.forget_window = Toplevel(self.root)
                        self.forget_window.title("Reset Password")
                        self.forget_window.geometry("400x350+500+100")
                        self.forget_window.focus_force()

                        title =Label (self.forget_window,text="Reset Password", font=("goudy old style",15,'bold'), bg="#3f51b5",fg="white").pack(side=TOP,fill=X)
                        lbl_reset=Label(self.forget_window,text="Enter OTP Sent on Registered Email", font=("times new roman",15)).place(x=20,y=60)
                        txt_reset=Entry(self.forget_window,textvariable=self.var_otp, font=("times new roman",15), bg="lightyellow").place(x=20,y=100,width=250,height=30)
                        
                        self.btn_reset = Button(self.forget_window, text="Submit", command=self.validate_otp, font=("times new roman", 15),
                                                bg="lightblue", cursor="hand2")
                        self.btn_reset.place(x=280, y=98, width=100, height=33)

                        lbl_new_pass = Label(self.forget_window, text="New Password",
                                        font=("times new roman", 15)).place(x=20, y=160)
                        txt_new_pass = Entry(self.forget_window, textvariable=self.var_new_pass, font=("times new roman", 15),
                                        bg="lightyellow").place(x=20, y=190, width=250, height=30)

                        lbl_confirm_pass = Label(self.forget_window, text="Confirm Password",
                                        font=("times new roman", 15)).place(x=20, y=225)
                        txt_confirm_pass = Entry(self.forget_window, textvariable=self.var_conf_pass, font=("times new roman", 15),
                                        bg="lightyellow").place(x=20, y=255, width=250, height=30)

                        self.btn_update = Button(self.forget_window, text="Update",command=self.update_password, state=DISABLED, font=("times new roman", 15),
                                                bg="lightblue", cursor="hand2")
                        self.btn_update.place(x=150, y=300, width=100, height=33)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
    
    def update_password(self):
        if self.var_new_pass.get()=="" or self.var_conf_pass.get()=="":
            messagebox.showerror("Error!!","Password is required.", parent=self.forget_window)

        elif self.var_new_pass.get()!= self.var_conf_pass.get():
            messagebox.showerror("Error!!", "Passwords must be same.", parent=self.forget_window)

        else:
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            try:
                cur.execute("Update employee SET pass=? where eid=?",(self.var_new_pass.get(),self.employee_id.get()))
                con.commit()
                messagebox.showinfo("Success!","Password Updated Successfully!!",parent=self.forget_window)
                self.forget_window.destroy()

            except Exception as ex:
                messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def validate_otp(self):
        if int(self.otp) == int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
        else:
            messagebox.showerror("Error!","Invalid OTP!!!",parent=self.forget_window)

    def send_email(self,to_):
        s = smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        email1 = email_pass.email_
        pass1 = email_pass.pass_

        s.login(email1, pass1)

        self.otp = int(time.strftime("%H%S%M"))+int(time.strftime("%S"))
        #print(self.otp)

        subject = 'Inventory Management System - Account Recovery'
        message= f'Dear Sir/Madam,\n\nYour Password Reset OTP is: {str(self.otp)}.\n\nWith Regards,\n\nInventory Management System-Team'
        message = "Subject:{}\n\n{}".format(subject,message)
        s.sendmail(email1, to_, message)
        check = s.ehlo()
        if check[0] == 250:
            return 'Success'
        else:
            return 'Failed'


root= Tk()
obj= loginSystem(root)
root.mainloop()


# python login.py