import sqlite3
import xlrd
from tkinter.ttk import *
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import webbrowser
from email.mime.multipart import MIMEMultipart
import smtplib
from email.mime.text import MIMEText


vkey='123456789'

#_____________________________________________Basic Things_____________________________________________________________
root=Tk()

root.geometry('600x600+0+0')
root.resizable(width=False,height=False)
root.configure(background="#000000")
icon="Result_Sender_Logo.png"
root.iconbitmap(icon)
root.title("Result Mailer")
#_________________________________________________________Database____________________________________________________________________


conn=sqlite3.connect('DontTouchit1.db')
cd=conn.cursor()
try:
    cd.execute('CREATE TABLE LOGIN (username text,password text,Recovery_key text)')
    #print('Sucessfully DB Created')
except Exception:
    pass

finally:

    #_________________________________________________DB CLOSE_______________________________________________________________________________


    #--------------------New Windows Funtions : on-----------------------------

    def Reset_fun():
        if len(username_entered.get())==0:
                messagebox.showerror('Reset Password','Please Enter Username')
        elif len(Recovery_key_entered.get())==0:
                messagebox.showerror('Reset Password','Please Enter Recovery Key')
        elif len(NewPassword1.get())==0:
                messagebox.showerror('Reset Password','Please Enter Password ')
        elif len(NewPassword2.get())==0:
                messagebox.showerror('Reset Password','Please Enter Password Again')
        else:
            try :
                global cd
                cd.execute("Select * from LOGIN where username='{}'".format(username_entered.get().upper()))
                xx=cd.fetchall()
                conn.commit()
                print(xx)
                print(xx[0][2])
                if xx:
                    if NewPassword1.get()==NewPassword2.get():
                        if xx[0][2]==Recovery_key_entered.get():
                            cd.execute("UPDATE LOGIN SET password='{}' WHERE username='{}'".format(NewPassword1.get(),username_entered.get().upper()))
                            conn.commit()
                            messagebox.showinfo('Reset Password','Sucessfully Reset')
                            global Reset_window
                            Reset_window.destroy()
                        else:
                            messagebox.showerror('Reset Password','Wrong Recovery Key')
                    else:
                        messagebox.showerror('Reset Password','Password Now Match')
            except Exception as e:
                messagebox.showerror('Reset Password','User Not Found')
            

    def Reset_page():
        global Reset_window
        Reset_window=Toplevel()
        Reset_window.geometry('600x600+0+0')
        Reset_window.resizable(width=False,height=False)
        Reset_window.configure(background="#000000")
        icon="D:/Jagdish_work/Python_Projects/Result_Sender/logo.ico"
        Reset_window.iconbitmap(icon)
        Reset_window.title("Result Mailer")

        global username_entered
        global Recovery_key_entered
        global NewPassword1
        global NewPassword2

        head=Label(Reset_window,text="Result Mailer ",bg='#000000',fg="#7C4521",font=' kalam 29 bold',pady=10)
        Reset_password_text=Label(Reset_window,text="Reset Password ",bg='#000000',fg='red',font=' kalam 28 bold',pady=8)
        username_text1=Label(Reset_window,text="Username :",bg='#000000',fg="#FC6604",font=' kalam 16 bold',pady=10)
        Recovery_key_text=Label(Reset_window,text="Recovery Key :",bg='#000000',fg="#FC6604",font=' kalam 16 bold',pady=10)

        username_entered=Entry(Reset_window,width=25,borderwidth=5,bg='#000000',fg="#FC6604",font=' kalam 14 ')
        Recovery_key_entered=Entry(Reset_window,width=25,borderwidth=5,bg='#000000',fg="#FC6604",font=' kalam 14 ',show='*')

        NewPassword_1_text=Label(Reset_window,text="New Password : ",bg='#000000',fg="#FC6604",font=' kalam 16 bold',pady=10)
        NewPassword1=Entry(Reset_window,width=25,borderwidth=5,bg='#000000',fg="#FC6604",font=' kalam 14 ',show='*')

        NewPassword_2_text=Label(Reset_window,text="Again New Password : ",bg='#000000',fg="#FC6604",font=' kalam 16 bold',pady=10)
        NewPassword2=Entry(Reset_window,width=25,borderwidth=5,bg='#000000',fg="#FC6604",font=' kalam 14 ')

        close_Reset=Button(Reset_window,text='Close',width=10,font='kalam 10 bold',fg='#040BFC',command=lambda:close('Reset_window'))
        Reset_button=Button(Reset_window,text='Reset',width=10,font=' kalam 10 bold',fg='#040BFC',command=Reset_fun)


        head.place(x=1,y=-5)
        Reset_password_text.place(x=240,y=50)
        username_text1.place(x=140,y=120)
        Recovery_key_text.place(x=120,y=170)
        username_entered.place(x=270,y=127)
        Recovery_key_entered.place(x=270,y=177)

        NewPassword1.place(x=270,y=240)  
        NewPassword_1_text.place(x=110,y=230)

        NewPassword_2_text.place(x=55,y=300)
        NewPassword2.place(x=270,y=300)

       
        Reset_button.place(x=200,y=400)

        
        close_Reset.place(x=340,y=400)



        Reset_window.mainloop()


    def close(y):
        close_value=messagebox.askokcancel('Result Mailer','Sure To Close')
        if close_value==1:
            if y=='root':
                root.destroy()
            elif y=='top':
                top.destroy()
            elif y=='Reset_window':
                Reset_window.destroy()
        else:
            pass

    def dynamic_widget(p,total,name):
        global progress_bar
        key_value=int(400/total)
        progress_bar['value'] = p*key_value
        top.update_idletasks()
        percentage=(p*100)/(total)
        send_percentages.configure(text='{}%'.format(percentage))
        status.configure(text='Sending Mail To {}'.format(name))

    def value(x,y):
        wb=xlrd.open_workbook(path)
        sheet=wb.sheet_by_index(0)
        return sheet.cell_value(x,y)

    def index_finder(x):
        
        for i in range(0,x):
            if value(0,i).upper()=='EMAIL'or value(0,i).upper()=='EMAIL ID':
                global email_index
                email_index=i
            if value(0,i).upper()=='NAME'or value(0,i).upper()=='STUDENT NAME':
                global name_index
                name_index=i
            if value(0,i).upper()=='ENROLLMENT' or value(0,i).upper()=='ENROLL':
                global  enroll_index
                enroll_index=i

    def open():
        top.filename=filedialog.askopenfilename(initialdir="",title="Select A E xcel File",filetypes=(("Excel File",".xlsx"),("All files",".*")))
        global path
        path=top.filename
        upload_value.delete(0,END)
        upload_value.insert(0,path)


    def send_mail(y):
        for j in range(1,y):
                global q
                senderid=user_email.get()
                password=user_password.get()
                print(senderid,password)
                msg=MIMEMultipart()
                server=smtplib.SMTP('smtp.gmail.com',587)
                server.starttls()
                server.login(senderid,password)
                mailto=value(j,email_index)
                print(mailto)
                msg['To']=mailto
                msg['From']=senderid
                msg['Subject']=subject.get()
                body='''<html>
                        <body>
                        <font color="red">
                        <center>
                        <h1>
                        {}
                        </center>
                        </h1>
                        </font>
                        <font color="Blue">
                        <h3>Name : {}
                        <br>Enrollment : {}<br>
                        Course : {}
                        <br> Branch :{} <br>
                        SEM : {} </h3>
                        </font>
                        <table border="1" style="width:100%">
                        <tr bgcolor="#B8FAF1" >
                        <th>Subject</th>
                        <th>Theory Marks</th>
                        <th>Quiz</th>
                        <th>Total</th>
                        </tr><tr>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                        </tr><tr>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                        </tr>  <tr>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                        </tr>  <tr>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                        </tr>  <tr>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                        <td>{}</td>
                        </tr></table>
                        <br>
                        <img src="http://netflixhacks.epizy.com/Mid-Result/S.jpg" width="150" height="120"><h3><font color="blue">
                        <br>
                        {}
                        </font>
                        </h3>
                        </body>
                        </html>'''.format(subject.get(),value(j,name_index).upper(),value(j,enroll_index),course.get(),branch.get(),sem.get(),value(0,3),value(j,3),value(j,4),value(j,3)+value(j,4),value(0,5),value(j,5),value(j,6),value(j,5)+value(j,6),value(0,7),value(j,7),value(j,8),value(j,7)+value(j,8),value(0,9),value(j,9),value(j,10),value(j,9)+value(j,10),value(0,11),value(j,11),value(j,12),value(j,11)+value(j,12),footer.get())
                msg.attach(MIMEText(body,'html'))
                text=msg.as_string()
                server.sendmail(senderid,mailto,text)
                dynamic_widget(q,y-1,value(j,name_index).upper())
                server.quit()
                q=q+1

    def Go():

        if len(subject.get())==0:
                messagebox.showerror('Result Mailer','Enter The Subject')
        elif len(footer.get())==0:
                messagebox.showerror('Result Mailer','Enter The Footer')
        elif len(course.get())==0:
                messagebox.showerror('Result Mailer','Enter The Course')
        elif len(sem.get())==0:
                messagebox.showerror('Result Mailer','Enter The Semester')
        elif len(branch.get())==0:
                messagebox.showerror('Result Mailer','Enter The Branch')
        else:

            try :
                global sheet
                wb=xlrd.open_workbook(path)
                sheet=wb.sheet_by_index(0)
                y=int(sheet.nrows)
                x=int(sheet.ncols)
                index_finder(x)
                send_mail(y)
                messagebox.showinfo("Sucessfull","All Messages Send Sucessfully")
            except smtplib.SMTPAuthenticationError:
                messagebox.showerror('Result Mailer','Enter Valid Email Id or Password or visit or help Section')
            except NameError: 
                messagebox.showerror('Result Mailer','Upload Excel File')
            except TypeError:
                messagebox.showerror('Result Mailer','Please Fill The Whole Details')
            except xlrd.biffh.XLRDError:
                messagebox.showerror('Result Mailer','Upload Valid Excel File')
            except smtplib.SMTPRecipientsRefused:
                messagebox.showerror('Result Mailer','There is Some Error in Excel File')
        
    def video():
        webbrowser.open('https://www.hallwick.in')

    def article():
        webbrowser.open('https://www.hallwick.in')

    def contact():
        webbrowser.open('https://www.hallwick.in/contact-us/')

    def about_us():
        webbrowser.open('https://www.hallwick.in/about-us/')

    def lightmode():
        global top
        top.configure(background="#ffffff")
        heading.configure(bg='#ffffff',fg='red',pady=25)
        user_email_text.configure(bg='#ffffff',fg='#000000')
        user_password_text.configure(bg='#ffffff',fg='#000000')
        subject_text.configure(bg='#ffffff',fg='#000000')
        Footer_text.configure(bg='#ffffff',fg='#000000')
        course_text.configure(bg='#ffffff',fg='#000000')
        sem_text.configure(bg='#ffffff',fg='#000000')
        branch_text.configure(bg='#ffffff',fg='#000000')
        user_email.configure(bg='#ffffff',fg='#000000')
        user_password.configure(bg='#ffffff',fg='#000000')
        subject.configure(bg='#ffffff',fg='#000000')
        footer.configure(bg='#ffffff',fg='#000000')
        course.configure(bg='#ffffff',fg='#000000')
        sem.configure(bg='#ffffff',fg='#000000')
        upload_value.configure(bg='#ffffff',fg='#000000')
        branch.configure(bg='#ffffff',fg='#000000')
        go.configure(image=go_image_light)
        close_Button.configure(image=close_image_light)
        send_percentages.configure(bg='#ffffff')
        status.configure(bg='#ffffff',fg="#000000")

    def darkmode():
        top.configure(background="#000000")
        heading.configure(bg='#000000',fg='red',pady=25)
        user_email_text.configure(bg='#000000',fg='#ffffff')
        user_password_text.configure(bg='#000000',fg='#ffffff')
        subject_text.configure(bg='#000000',fg='#ffffff')
        Footer_text.configure(bg='#000000',fg='#ffffff')
        course_text.configure(bg='#000000',fg='#ffffff')
        sem_text.configure(bg='#000000',fg='#ffffff')
        branch_text.configure(bg='#000000',fg='#ffffff')
        user_email.configure(bg='#000000',fg='#ffffff')
        user_password.configure(bg='#000000',fg='#ffffff')
        subject.configure(bg='#000000',fg='#ffffff')
        footer.configure(bg='#000000',fg='#ffffff')
        course.configure(bg='#000000',fg='#ffffff')
        sem.configure(bg='#000000',fg='#ffffff')
        upload_value.configure(bg='#000000',fg='#ffffff')
        branch.configure(bg='#000000',fg='#ffffff')
        go.configure(image=go_image_dark)
        close_Button.configure(image=close_image_dark)
        send_percentages.configure(bg='#000000')
        status.configure(bg='#000000',fg="#ffffff")

    def clear():
        clear_value=messagebox.askokcancel('Result Mailer','Clear Everything')
        if clear_value==1:
            subject.delete(0,END)
            footer.delete(0,END)
            sem.delete(0,END)
            course.delete(0,END)
            branch.delete(0,END)
            user_email.delete(0,END)
            user_password.delete(0,END)
            global progress_bar
            global percentage
            progress_bar['value'] =0
            send_percentages.configure(text='{}%'.format(0))
            status.configure(text='')
        else:
            pass

    def logout():
            x=messagebox.askokcancel('Result Mailer','Sure To Logout')
            if x==1:
                top.destroy() 
            else:
                pass
    def Profile():
        pass
    def Change_password():
        pass

    def new_window():
        global root
        root.destroy()
        global top
        top=Tk()
        
        
        #definign Window
        top.geometry('630x630+0+0')
        top.resizable(width=False,height=False)
        top.configure(background="#000000")

        #defining Title,bgcolor
        top.title("Result Mailer")  
        
        
        #images
        
        
        global go_image_light
        global close_image_dark
        global go_image_dark
        global close_image_light

        go_image_dark=PhotoImage(file="D:/Jagdish_work/Python_Projects/Result_Sender/go_dark.png")
        close_image_dark=PhotoImage(file="D:/Jagdish_work/Python_Projects/Main_Sender/close_dark.png")
        go_image_light=PhotoImage(file="D:/Jagdish_work/Python_Projects/Result_Sender/go_light.png")
        close_image_light=PhotoImage(file="D:/Jagdish_work/Python_Projects/Main_Sender/close_light.png")
        global icon2
        icon2="D:/Jagdish_work/Python_Projects/Result_Sender/logo.ico"
        top.iconbitmap(icon2)
        global heading
        heading = Label(top,text='Result Mailer ',font=' kalam 28 bold',bg='#000000',fg='red',pady=25)
        heading.grid(row=0,column=2)
        #-----------------------------------Progress Bar---------------
        global progress_bar
        progress_bar = Progressbar(top, orient = HORIZONTAL, length = 400, mode = 'determinate',) 

        #percentage
        global send_percentages
        send_percentages=Label(top,text='{}%'.format(0),bg='#000000',font=' times 16 bold',fg="#ff0000",pady=8)
        send_percentages.grid(row=10,column=3)

        #-----------------Defining Text------------------------------------------------------
        global user_email_text
        global user_password_text
        global subject_text
        global Footer_text
        global course_text
        global sem_text
        global branch_text



        user_email_text=Label(top,text="You Email Address : ",bg='#000000',fg="#ffffff",font=' times 16 bold',pady=8)
        user_password_text=Label(top,text="Password : ",bg='#000000',fg="#ffffff",font=' times 16 bold',pady=8)
        subject_text=Label(top,text="Subject : ",bg='#000000',fg="#ffffff",font=' times 16 bold',pady=8)
        Footer_text=Label(top,text="Footer of the Mail : ",bg='#000000',fg="#ffffff",font=' times 16 bold',pady=8)
        course_text=Label(top,text="Course :",bg='#000000',font=' times 16 bold',fg="#ffffff",pady=8)
        sem_text=Label(top,text="Semester :",bg='#000000',font=' times 16 bold',fg="#ffffff",pady=8)
        branch_text=Label(top,text="Branch : ",bg='#000000',font=' times 16 bold',fg="#ffffff",pady=8)


        #_____________________defining Buttons____________________________________________
        global go
        global close_Button
        global upload_file
        go=Button(top,image=go_image_dark,height=50,width=2,border=0,command=Go)
        close_Button=Button(top,image=close_image_dark,height=50,width=11,border=0,command=lambda:close('top'))
        upload_file=Button(top,text="Upload Excel File : ",command=open)

        #____________________Definging Entry Widgets___________________________

        global user_email
        global user_password
        global subject
        global footer
        global course
        global sem
        global upload_value
        global branch
        global status

        user_email=Entry(top,width=45,borderwidth=5,bg='#000000',fg="#ffffff",font='times 12 ')
        user_password=Entry(top,width=45,borderwidth=5,show='*',bg='#000000',fg="#ffffff",font=' times 12')
        subject=Entry(top,width=45,borderwidth=5,bg='#000000',fg="#ffffff",font=' times 12')
        footer=Entry(top,width=45,borderwidth=5,bg='#000000',fg="#ffffff",font=' times 12 ')
        course=Entry(top,width=30,borderwidth=5,bg='#000000',fg="#ffffff",font=' times 12 ')
        sem=Entry(top,width=30,borderwidth=5,bg='#000000',fg="#ffffff",font=' times 12 ')
        upload_value=Entry(top,width=20,bg='#000000',fg="#ffffff",font=' times 12 ')
        branch=Entry(top,width=30,borderwidth=5,bg='#000000',fg="#ffffff",font=' times 12 ')
        status=Label(top,bg='#000000',fg="#ffffff",font=' times 12')

        subject.insert(0,'Midturm Result 2020')
        footer.insert(0,'CSE Department,Rewa Engineering College Rewa')
        sem.insert(0,"4th")
        course.insert(0,"B.Tech")
        branch.insert(0,"CSE")
        upload_value.insert(0,"Path of File")

        #-----------------------------------------------------------showing Text------------------------------------------------------------------------------------------
        
        user_email_text.grid(row=1,column=1)
        user_password_text.grid(row=2,column=1)
        subject_text.grid(row=3,column=1)
        Footer_text.grid(row=4,column=1)
        course_text.grid(row=5,column=1)
        sem_text.grid(row=6,column=1)
        branch_text.grid(row=7,column=1)
        upload_file.grid(row=9,column=2)

    #----------------------------------------------------------showing Buttons---------------------------------------------------------------------------------------

        close_Button.grid(row=11,column=2,pady=15,ipadx=40)
        go.grid(row=11,column=3,pady=15,ipadx=40)
        progress_bar.grid(row=10,column=1,pady=10,columnspan=2)
        status.grid(row=11,column=0,columnspan=2)

    #-------------------------------------------------------------Showing Entry Widgets--------------------------------------------------------------------------
        user_email.grid(row=1,column=2,columnspan=2)
        user_password.grid(row=2,column=2,columnspan=2)
        subject.grid(row=3,column=2,columnspan=2)
        footer.grid(row=4,column=2,columnspan=2)
        course.grid(row=5,column=2)
        sem.grid(row=6,column=2)
        branch.grid(row=7,column=2)
        upload_value.grid(row=8,column=2)


    #------------------------Main Menu  : On -------------------------------
        main_menu=Menu()
        Account=Menu(main_menu,tearoff=False)
        Edit=Menu(main_menu,tearoff=False)
        Theme=Menu(main_menu,tearoff=False)

        Help=Menu(main_menu,tearoff=False)
        about=Menu(main_menu,tearoff=False)


        Account.add_command(label='Profile',command=Profile)
        Account.add_command(label='Change Password',command=Change_password)
        Account.add_command(label='Logout',command=logout)
        Account.add_command(label='Close',command=lambda:close('top'))
        Edit.add_command(label='Clear',command=clear)
        Theme.add_command(label='Dark Theme',command=darkmode)
        Theme.add_command(label='Light Theme',command=lightmode)

        Help.add_command(label="Watch Video",command=video)
        Help.add_command(label='Read Article',command=article)
        Help.add_command(label='Contact Us',command=contact)
        about.add_command(label='About App',command=about_us)


        #cascading
        main_menu.add_cascade(label='Account',menu=Account)
        main_menu.add_cascade(label='Edit',menu=Edit)
        main_menu.add_cascade(label='Theme',menu=Theme)
        main_menu.add_cascade(label='Help',menu=Help)
        main_menu.add_cascade(label='About',menu=about)



        #--------------------------------------------------Main Menu : Off-------------------------------------------




        
        top.config(menu=main_menu)

        top.mainloop()


        #-------------------------------New Windows Functions :Off------------------------------


    def login_1(u,p):
        cd.execute("Select * from LOGIN where username='{}'".format(u.upper()))
        #cd.fetchone()[0][0]
        try :
            pass_word=cd.fetchall()[0][1]
            if pass_word:
                if pass_word==p:
                    print('Sucussfully Login')
                    messagebox.showinfo("Login","Sucessfully Login")
                    new_window()
   
                else:
                    print('Password Not Match')
                    messagebox.showerror('Login','Incorrect Password')
        except Exception as e:
            messagebox.showerror('Login','Username Not Found')
        conn.commit()

    def signup_page():
        if len(username_enter.get())==0:
                messagebox.showerror('SignUp','Please Enter Username')
        elif len(password1.get())==0:
                messagebox.showerror('SignUp','Please Enter Password')
        elif len(again_password.get())==0:
                messagebox.showerror('SignUp','Please Enter Password Again')
        #elif len(Email.get())==0:
        #        messagebox.showerror('SignUp','Please Enter The Email Id')
        #elif len(Email_Password.get())==0:
        #        messagebox.showerror('SignUp','Please Enter The Email Password')
        elif(len(Validation_key.get()))==0:
            messagebox.showerror('SignUp','Please Enter Validation Key')
        elif len(Recovery_key.get())==0:
            messagebox.showerror('SignUp','Please Enter Recovery Key')
        elif CheckVar1.get()==0:
            messagebox.showerror('Signup','Check The Checkboxes')
        elif Validation_key.get()!=vkey:
            messagebox.showerror('Signup','Wrong Validation Key')
            
        else:
            cd.execute("Select * from LOGIN where username='{}'".format(username_enter.get().upper()))
            value=cd.fetchall()
            conn.commit()
            print(value)   
            if value:
                messagebox.showerror('Login','User Already Exist')
                print(value[0][0])
            elif password1.get()!=again_password.get():
                messagebox.showerror('Login','Password Not Match')
            else:
                cd.execute("insert into LOGIN VALUES('{}','{}','{}')".format(username_enter.get().upper(),password1.get(),Recovery_key.get()))
                messagebox.showinfo("Signup","Sucessfully Signup")
                username_enter.delete(0,END)
                password1.delete(0,END)
                
                login_0()


                conn.commit()
        
    #_____________________________________________________________________________________________________________________________

    def help():
        webbrowser.open('https://www.hallwick.in/about-us/')

    def hide(x):
        x.place(x=-100,y=-100)


    def Creat_New_Account():
    
        #_____________________-------Hiding---------_________________________
        hide(login)
        hide(close_login)
        hide(Reset_password)
        hide(Creat_account)
        #------------------__________________Showing_______________--------------

        #Placing
        Login_text.configure(text='Creat New Account')
        Login_text.place(x=210,y=60)
        again_password.place(x=270,y=240)  
        again_password_text.place(x=100,y=230)


        Validation_key_text.place(x=100,y=280)
        Validation_key.place(x=270,y=300)
        #Email_Password_Text.place(x=100,y=350)
        #Email_Password.place(x=270,y=350)



        Recovery_key_text.place(x=120,y=350)
        Recovery_key.place(x=270,y=350)
        

        C1.place(x=240,y=450)
        C2.place(x=240,y=490)


        Signup.place(x=320,y=540)
        Close.place(x=420,y=540)
        Login_0.place(x=110,y=540)
        help1.place(x=210,y=540)

    def login_0():
        Login_text.configure(text='Login')
        Login_text.place(x=240,y=50)

        #---------------------------Hiding---------

        hide(again_password)
        hide(again_password_text)
        #login.destroy()
        #close_login.destroy()


        hide(Validation_key)
        hide(Validation_key_text)
        #hide(Email_Password_Text)
        #hide(Email_Password)
        hide(C1)
        hide(C2)


        #Reset_password.destroy()
        #Creat_account.destroy()

        hide(Recovery_key_text)
        hide(Recovery_key)

        hide(Signup)
        hide(Close)
        hide(Login_0)
        hide(help1)
        hide(again_password_text)

        global login
        global close_login
        global Reset_password
        global Creat_account
        login=Button(root,text='Login',width=10,font=' kalam 10 bold',fg='#040BFC',command=lambda:login_1(username_enter.get(),password1.get()))
        login.place(x=200,y=300)

        close_login=Button(root,text='Close',width=10,font='kalam 10 bold',fg='#040BFC',command=lambda:close('root'))
        close_login.place(x=340,y=300)
        Reset_password=Button(root,text='Reset Password ? ',width=20,font=' kalam 10 bold',fg='#040BFC',command=Reset_page)
        Reset_password.place(x=10,y=370)
        Creat_account=Button(root,text=' Creat A New Account ',width=20,font=' kalam 10 bold',fg='#040BFC',command=Creat_New_Account)
        Creat_account.place(x=10,y=420)

    
#__________________________________________________________PResend widgets__________________________________________________________________

    Login_text=Label(root,text="Login ",bg='#000000',fg='red',font=' kalam 28 bold',pady=8)
    heading1=Label(root,text="Result Mailer ",bg='#000000',fg="#7C4521",font=' kalam 29 bold',pady=10)
    username_text=Label(root,text="Username :",bg='#000000',fg="#FC6604",font=' kalam 16 bold',pady=10)
    password1_text=Label(root,text="Password :",bg='#000000',fg="#FC6604",font=' kalam 16 bold',pady=10)
    again_password_text=Label(root,text="Again Password :",bg='#000000',fg="#FC6604",font=' kalam 16 bold',pady=10)
    username_enter=Entry(root,width=25,borderwidth=5,bg='#000000',fg="#FC6604",font=' kalam 14 ')
    password1=Entry(root,width=25,borderwidth=5,bg='#000000',fg="#FC6604",font=' kalam 14 ',show='*')
    again_password=Entry(root,width=25,borderwidth=5,bg='#000000',fg="#FC6604",font=' kalam 14 ',show='*')


    Validation_key_text=Label(root,text="Validation Key :",bg='#000000',fg="#FC6604",font=' kalam 16 bold',pady=10)
    Validation_key=Entry(root,width=25,borderwidth=5,bg='#000000',fg="#FC6604",font=' kalam 14 ')
    #Email_Password_Text=Label(root,text="Email Password : ",bg='#000000',fg="#FC6604",font=' kalam 16 bold',pady=10)
    #Email_Password=Entry(root,width=25,borderwidth=5,bg='#000000',fg="#FC6604",font=' kalam 14 ',show='*')


    login=Button(root,text='Login',width=10,font=' kalam 10 bold',fg='#040BFC',command=lambda:login_1(username_enter.get(),password1.get()))
    close_login=Button(root,text='Close',width=10,font='kalam 10 bold',fg='#040BFC',command=lambda:close('root'))
    Reset_password=Button(root,text='Reset Password ? ',width=20,font=' kalam 10 bold',fg='#040BFC',command=Reset_page)
    Creat_account=Button(root,text=' Creat A New Account ',width=20,font=' kalam 10 bold',fg='#040BFC',command=Creat_New_Account)



    Signup=Button(root,text='Signup',width=10,font='kalam 10 bold',fg='#040BFC',command=signup_page)
    Close=Button(root,text='Close' ,width=10,font=' kalam 10 bold',fg='#040BFC',command=lambda:close('root'))
    Login_0=Button(root,text='Login',width=10,font='kalam 10 bold',fg='#040BFC',command=login_0)
    help1=Button(root,text='Help ',width=10,font=' kalam 10 bold',fg='#040BFC',command=help)


    Recovery_key_text=Label(root,text="Recovery Key :",bg='#000000',fg='#FC6604',font=' kalam 16 bold',pady=8)
    Recovery_key=Entry(root,width=25,borderwidth=5,bg='#000000',fg="#FC6604",font=' kalam 14 ',show='*')








    #-------------------------------------------------------CheckBoxes-----------------------------------------------------------
    CheckVar1 = IntVar()
    C1 = Checkbutton(root, text = "I have Set SMTP Settings", variable = CheckVar1, onvalue = 1, offvalue = 0, bg='#000000',fg="#FC6604")
    C2 = Checkbutton(root, text = "I Agree to All T&C", variable = CheckVar1,onvalue = 1, offvalue = 0,bg='#000000',fg="#FC6604")


    #_______________________________________________________________placing____________________________________________________

    heading1.place(x=1,y=-5)
    Login_text.place(x=240,y=50)
    username_text.place(x=140,y=120)
    password1_text.place(x=140,y=170)
    username_enter.place(x=270,y=127)
    password1.place(x=270,y=177)



    login.place(x=200,y=250)
    close_login.place(x=340,y=250)
    Reset_password.place(x=10,y=370)
    Creat_account.place(x=10,y=420)




    root.mainloop()
    #_________________________________________________________________________________________________________________________







  


   
