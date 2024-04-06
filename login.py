import tkinter 
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image

from utils import error 

class Login:
    """Represents a login window for user authentication."""
    def __init__(self, con):
        ctk.set_default_color_theme("dark-blue")
        ctk.set_appearance_mode("dark")
        self.window =  ctk.CTk() 
        self.window.title("Sign In")
        self.window.geometry("500x600")
        self.con = con
        self.cur = con.cursor()
        self.user = None
        self.login_window()

    def login_window(self, event=None):
        """ Function to create login window."""
        self.window.title("Sign In")
        self.window.bind('<Return>', self.login)
        
        img = ctk.CTkImage(dark_image = Image.open("./imgs/bg.jpg").resize((500,600)),size=(500,600))
        bg = ctk.CTkLabel(master=self.window,image=img)
        bg.place(x=0,y=0)

        self.frame = ctk.CTkFrame(master=bg, width=320, height=360, corner_radius=15)
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.login_label = ctk.CTkLabel(master=self.frame, text="Log in", font=('Century Gothic',30))
        self.login_label.place(x=100, y=45)

        self.username = ctk.CTkEntry(master=self.frame, width=220, placeholder_text='Username')
        self.username.place(x=50, y=110)

        self.password = ctk.CTkEntry(master=self.frame, width=220, placeholder_text='Password', show="*")
        self.password.place(x=50, y=165)

        self.label_link = ctk.CTkLabel(master=self.frame, text="Don't have an account? Register",font=('Century Gothic',13))
        self.label_link.place(x=60,y=210)
        self.label_link.bind("<Button-1>", self.register_window)

        # Create Login button
        button = ctk.CTkButton(master=self.frame, width=220, text="Login", command=self.login, corner_radius=6)
        button.place(x=50, y=250)

    def register_window(self, event=None):
        """ Function to display register window."""
        self.window.title("Create an account")
        self.window.bind('<Return>',self.register)
        self.login_label.configure(text="Register")
        self.label_link.configure(text="Already have an Account? Sign in")
        self.label_link.bind("<Button-1>", self.login_window)
        button = ctk.CTkButton(master=self.frame, width=220, text="Continue", command=self.register, corner_radius=6)
        button.place(x=50, y=250)
        
    

    def login(self, event=None):
        """Authenticate the user by checking the provided username and password with MySQL. """
        uname = self.username.get()
        pwd = self.password.get()
        self.cur.execute("INSERT IGNORE INTO users (username, password, account_type) VALUES ('ADMIN', 'ADMIN', 'ADMIN');")
        self.cur.execute(f"select * from users where username='{uname}' and password='{pwd}' ")
        f = self.cur.fetchall()
        if f:
            print("└─Logged in as {}".format(uname))
            self.window.quit()
            self.user = f[0]

        else:
            error("Invalid Username or Password")

    def register(self):
        """Create a new user account by registering the provided username and password in MySQL. """
        uname = self.username.get()
        pwd = self.password.get()
        
        
        self.cur.execute(f"select * from users where username='{uname}'")
        f = self.cur.fetchall()
        if f:
            error("Username already exist")

        else:    
            if(len(uname) == 0 or len(pwd) == 0):
                error("Length of the Username and Password should be greater than 0")
                return
            elif len(uname)>20 or len(pwd)>20 :
                error("Length of the Username and Password should be less than 20")
                return
                    
            self.cur.execute(f"insert into users values('{uname}','{pwd}','USER')")
            self.con.commit()
            messagebox.showinfo("Account created", "Your account has been succesfully created!")
            self.window.quit()
            self.user = (uname, pwd, 'USER')