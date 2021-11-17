import tkinter as tk
from tkinter import *
import HelloWorld_functions as mf
import pandas as pd
import difflib
from PIL import ImageTk,Image


df = pd.read_excel(r'Food List.xlsx')
stage = 1
temp = ""
buttons ={}
back_button = {}
item_list = []
faq_Ques = []


#When "enter" key is pressed , send() function is executed
def enter(a):
    send()
    return "break"


#send() is executed when, enter key or send button is pressed to send message
def send():
    global stage
    global temp
    global item_list
    global faq_Ques
    msg = EntryBox.get("1.0",'end-1c').strip() 
    EntryBox.delete("0.0",END)

    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Courier New", 10 ))
        res , stage , temp , item_list, faq_Ques= mf.chatbot_response(msg,df,stage,temp,item_list,faq_Ques)
        if temp == "clear":
            ChatLog.delete("0.0",END)
            temp = []
        ChatLog.insert(END, "Bot: " + res + '\n\n')
        destroyButtons()
        destroybackButton()
        createButtons(stage)
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)
        if(stage!=1):
            createBackButton()
        
        
#Update the entry_box text
def entry_update(text):
    EntryBox.delete("1.0",END)
    EntryBox.insert("1.0",text)

#Create buttons of suggested answer for different types of stages
def createButtons(stage):
    global option
    
    if stage == 1:
        option =[]
        option1 = ["Recommendation","Order","FAQ"]
        option = option1
        for i in option:
            def buttonFunc(x=i):
                return entry_update(x)

            if(i!="Recommendation"):
                buttons[i] = Button(frame, font=("Verdana",10,'bold'), text=i, width=20, height=2,
                         bd=1, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',command=buttonFunc )
                buttons[i].pack()
            else:
                buttons[i] = Button(frame, font=("Verdana",10,'bold'), text=i, width=20, height=2,
                         bd=1, bg="#263BF7", activebackground="#8DE5FF",fg='#ffffff',command=recommendation)
                buttons[i].pack()
                

    elif stage == 2:
        option =[]
        option2 = ["Malay","Mamak","Beverage","Korean","Japanese","Sort by price","Sort by deliverability"]
        option = option2
        for i in option:
            if option.index(i) < 5:
                def buttonFunc(x = "Please show me the "+i+" menu"):
                    return entry_update(x)
            else :
                def buttonFunc(x = i):
                    return entry_update(x)
            buttons[i] = Button(frame, font=("Verdana",10,'bold'), text=i, width=20, height=2,
                            bd=1, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',command=buttonFunc )
            buttons[i].pack()
        
        
    elif stage == 3:
        option =[]
        option3 = ["Low to High","High to Low"]
        option = option3
        for i in option:
            def buttonFunc(x = i):
                return entry_update(x)
            buttons[i] = Button(frame, font=("Verdana",10,'bold'), text=i, width=20, height=2,
                         bd=1, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',command=buttonFunc )
            buttons[i].pack()

    elif stage == 4:
        option =[]
        option3 = ["Low to High","High to Low"]
        option = option3
        for i in option:
            def buttonFunc(x = i):
                return entry_update(x)
            buttons[i] = Button(frame, font=("Verdana",10,'bold'), text=i, width=20, height=2,
                         bd=1, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',command=buttonFunc )
            buttons[i].pack()

    elif stage == 5:
        
        option = []
        option = mf.sugg
        if(len(option) < 3):
            for i in option:
                def buttonFunc(x = i):
                    return entry_update(x)
                buttons[i] = Button(frame, font=("Verdana",10,'bold'), text=i, width=20, height=2,
                         bd=1, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',command=buttonFunc )
                buttons[i].pack()
        else:       
            for i in option:
                def buttonFunc(x = i):
                    return entry_update(x)
                buttons[i] = Button(frame, font=("Verdana",10,'bold'), text=i, width=20, height=2,
                             bd=1, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',command=buttonFunc )
                buttons[i].pack()
        
    elif stage == 7:
        option = []
        option7 = ["Continue Shopping","Go to checkout"]
        option = option7
        for i in option:
            def buttonFunc(x = i):
                return entry_update(x)
            buttons[i] = Button(frame, font=("Verdana",10,'bold'), text=i, width=20, height=2,
                         bd=1, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',command=buttonFunc )
            buttons[i].pack()

    elif stage == 9:
        option = []
        option9 = ["Add other items","Remove item","Confirm Order"]
        option = option9
        for i in option:
            def buttonFunc(x = i):
                return entry_update(x)
            buttons[i] = Button(frame, font=("Verdana",10,'bold'), text=i, width=20, height=2,
                         bd=1, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',command=buttonFunc )
            buttons[i].pack()

    elif stage == 10:
        option = []
        option = list(dict.fromkeys(item_list))
        for i in option:
            def buttonFunc(x = df["item_name"][i]):
                return entry_update(x)
            buttons[i] = Button(frame, font=("Verdana",10,'bold'), text=df["item_name"][i], width=20, height=2,
                         bd=1, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',command=buttonFunc )
            buttons[i].pack()
    elif stage == 12:
        option = []
        option1 = ["Delivery","Self Pick-Up"]
        option2 = ["Self Pick-Up"]
        for i in item_list:
            if(df["delivery_service"][i]=="no"):
                option = option2
                break;
            else:
                option = option1
        for i in option:
            def buttonFunc(x = i):
                return entry_update(x)
            buttons[i] = Button(frame, font=("Verdana",10,'bold'), text=i, width=20, height=2,
                         bd=1, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',command=buttonFunc )
            buttons[i].pack()
            
    elif stage == 14:
        base.destroy()
        quit()

    elif stage == 15:
        option = []
        option15 = ["1","2","3","4","5","6"]
        option = option15
        for i in option:
            def buttonFunc(x = i):
                return entry_update(x)
            buttons[i] = Button(frame, font=("Verdana",10,'bold'), text=i, width=20, height=2,
                         bd=1, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',command=buttonFunc )
            buttons[i].pack()

    
        
            
        
       

    
   
#Destroy suggested answer buttons so that they can be replaced by new buttons        
def destroyButtons():
    for i in option:
        buttons[i].destroy()

#Create "Go Back" button
def createBackButton():
    def buttonFunc(x = "Go back"):
        return entry_update(x)
    back_button[0] = Button(frame, font=("Verdana",10,'bold'), text="Go back", width=20, height=2,
                         bd=1, bg="#ff0000", activebackground="#f78d8d",fg='#ffffff',command=buttonFunc )
    back_button[0].pack()

#Destroy "Go Back" button
def destroybackButton():
    if(back_button):
        back_button[0].destroy()

#Create "My Cart" button to check current item list
def createCartButton():
    cartButton = Button(frame, font=("Verdana",10,'bold'), text="My Cart", width=20, height=2,
                         bd=1, bg="#b0c930", activebackground="#d4eb60",fg='#ffffff',command=popupCart )
    cartButton.pack()

#Create pop-up window for recommendation food list
def recommendation():
    popupPicture = Toplevel()
    popupPicture.wm_title("Recommendations")
    popupPicture.grab_set()
    positionRight = int(base.winfo_screenwidth()/2 - 550/2)
    #positionDown = int(base.winfo_screenheight()/2 - 400/2)
    positionDown = 10
    popupPicture.geometry("550x750"+"+"+str(positionRight)+"+"+str(positionDown))

    

    recommended_list = ["Nasi Goreng Pattaya","Satay","Maggi Goreng","Roti Canai","Teriyaki Chicken Bento","Gyoza","Kimchi Fried Rice",
                        "Tteokbokki","Orange Juice"]
    cuisine_list = ["Malay","Malay","Mamak","Mamak","Japanese","Japanese","Korean","Korean","Beverage"]
    pic_c = 0
    pic_r = 1
    name_c = 0
    name_r = 2
    cuisine_c = 0
    cuisine_r = 0
    for i in recommended_list:
        img = Image.open("image_lib/"+i+".jpg")
        resized_image= img.resize((175,175), Image.ANTIALIAS)
        new_image= ImageTk.PhotoImage(resized_image)
        label = Label(popupPicture, image=new_image, bd = 2)
        label.image = new_image
        label.grid(row = pic_r, column = pic_c, pady = 2, padx = 2)
        name = Label(popupPicture, text = i, bd = 2, fg = "black", font = ("Courier New", 10))
        name.grid(row = name_r, column = name_c, pady = 2, padx = 2)
        if(pic_c < 2):
            pic_c += 1
            name_c +=1
        else:
            blank = Label(popupPicture, text = "", bd = 2, fg = "black", font = ("Courier New", 10))
            blank.grid(row = pic_r + 2, column = 0, pady = 2, padx = 2)
            pic_c = 0
            pic_r += 5
            name_c = 0
            name_r +=5
    for i in cuisine_list:
        cuisine = Label(popupPicture, text = i, bd = 2, fg = "black", font = ("Courier New", 10))
        cuisine.grid(row = cuisine_r, column = cuisine_c, pady = 2, padx = 2) 
        if(cuisine_c < 2):
            cuisine_c += 1
        else:
            cuisine_c = 0
            cuisine_r += 5

#Create pop-up window for the cart
def popupCart():
    popupCart = Toplevel()
    popupCart.wm_title("My Cart")
    popupCart.grab_set()
    positionRight = int(base.winfo_screenwidth()/2 - 500/2)
    positionDown = int(base.winfo_screenheight()/2 - 400/2)
    popupCart.geometry("500x400"+"+"+str(positionRight)+"+"+str(positionDown))
    cart = Text(popupCart, bd=0, bg="white", height="24", width="60", font=("Courier New", 10))
    cart.place(relx=0.015,rely=0.015)
    cart_scrollbar = Scrollbar(popupCart, command=cart.yview)
    cart_scrollbar.pack(side=RIGHT, fill=Y)
    cart['yscrollcommand'] = cart_scrollbar.set
    cart.insert(END,"{:<25} {:<23} {}\n\n\n".format("Item Name","Quantity","Price"))
    price_list =[]
    price_total = 0
    my_count=[[x,item_list.count(x)] for x in set(item_list)]
    for i in range(0,len(my_count)):
        index = my_count[i][0]
        quantity = my_count[i][1]
        price = float(quantity) * float(df['price'][index])
        price=round(price,2)
        price_list.append(price)
        cart.insert(END,"{:<28} {:<20} {}\n\n".format(df["item_name"][index],str(quantity),"RM"+str(price)))
    for j in price_list:
        price_total = price_total + j
    if(price_list):
        cart.insert(END,"\n\n\n\n\n\n\n\nTotal Price: RM"+str(price_total))
    
    cart.config(state=DISABLED)

#Create base of the GUI
base = Tk()
base.title("Food Ordering Bot")
positionRight = int(base.winfo_screenwidth()/2 - 850/2)
positionDown = int(base.winfo_screenheight()/2 - 700/2)
base.geometry("900x700"+"+"+str(positionRight)+"+"+str(positionDown))
base.resizable(width=FALSE, height=FALSE)


#Create Chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial")

ChatLog.config(foreground="#442265", font=("Courier New", 10 ))
ChatLog.insert(END, "Bot: " + "Hi, nice to meet you" + '\n\n')
ChatLog.insert(END, "Bot: " + "How can I help you?" + '\n\n')
ChatLog.config(state=DISABLED)

#Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview)
ChatLog['yscrollcommand'] = scrollbar.set

#Create Button to send message
SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="12", height=5,
                    bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                    command= send )

#Create the box to enter message
EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")
EntryBox.bind("<Return>", enter) # <Return> represents the enter button on keyboard



#frame
frame = Frame(base)
frame.place(x=700,y=6,height=580,width=200)

#buttons
createCartButton()
createButtons(stage)

#draw colored square for instructions
w = Canvas(base, width = 200, height = 150)
w.create_rectangle(5,5,15,15,fill="#b0c930",outline="#b0c930")
w.create_text(60,10,text="Display Cart")
w.create_rectangle(5,35,15,45,fill="#263BF7",outline="#263BF7")
w.create_text(55,40,text="Best Seller")
w.create_rectangle(5,65,15,75,fill="#32de97",outline="#32de97")
w.create_text(80,70,text="Suggested Answers")
w.create_rectangle(5,95,15,105,fill="#ff0000",outline="#ff0000")
w.create_text(42,100,text="Back")
                        
   

#Place all components on the screen
scrollbar.place(x=676,y=6, height=580)
ChatLog.place(x=6,y=6, height=580, width=670)
EntryBox.place(x=6, y=600, height=90, width=694)
SendButton.place (x= 700 , y = 600, height=90 , width = 190)
w.place(x=700,y=420)


base.mainloop()



    
