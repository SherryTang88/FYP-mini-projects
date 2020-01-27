from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from functools import partial
import pandas as pd
from datetime import date
import datetime
import sys
import argparse

canteen =''
store = ''
#input database as save data in a dataframe
def input_args(database):

    menu = pd.read_csv(database)

    for index, row in menu.iterrows():
        row['start_time']=datetime.time(row['start_hour'],row['start_min'])
        menu['start_time']=row['start_time']
        row['end_time']=datetime.time(row['end_hour'],row['end_min'])
        menu['end_time']=row['end_time']

    return menu

#get current day and time
def get_time_day():
    weekday = datetime.datetime.today().weekday()
    timenow = datetime.datetime.now().time()

    return weekday,timenow


def show_menu_logic(df_store):
    weekday,timenow = get_time_day()
    df_available = df_store.loc[df_store['day']==weekday]
    df_available=df_available.loc[df_available['start_time']<timenow]
    df_available=df_available.loc[df_available['end_time']>timenow]

    food_list  = df_available.to_dict('records')

    return food_list


#for reference only, the function used to get the dish images
def resize_image(image):
    img = Image.open(image) 
    new_width  = 150
    new_height = 150
    img = img.resize((new_width, new_height), Image.ANTIALIAS)
    img.save("new_can.png")
    

def root_window():
    canvas=Canvas(root,width=400,height=500)
    canvas.place(x = 0, y = 0)
    img1=PhotoImage(file='output image name.png')
    l1 = Label(canvas,image =img1,borderwidth=0)
    l1.image = img1
    l1.pack()
    b1 =Button(root, text = "I WANT FOOD", width = 15, height =2, command = select_canteen)
    b1.place(x= 142,y= 380)


def get_canteen_list(menu):
    can_choices = list(set(menu.canteen_name.tolist()))
    return can_choices


def get_store_list(df_canteen):
    store_choices = list(set(df_canteen.canteen_store.tolist()))
    return store_choices

def CurSelet(listbox):
    selection=listbox.curselection()[0]
    global canteen
    canteen = listbox.get(selection)

def CurSeletStore(listbox):
    selection=listbox.curselection()[0]
    global store
    store = listbox.get(selection)
    
def select_canteen():
    menu = input_args("menu_database.csv")
    frm_canteen =Frame(root,width = 400,height =200)
    frm_canteen.pack_propagate(0)
    frm_canteen_bottom =Frame(root,width = 400,height =300)
    frm_canteen_bottom.pack_propagate(0)
    frm_canteen.pack()
    frm_canteen_bottom.pack(side = BOTTOM)
    photo1=PhotoImage(file='new_can.png')
    l2 = Label(frm_canteen,image =photo1,borderwidth=0)
    l2.image = photo1
    l2.pack(side=RIGHT,padx=20)
    l1= Label(frm_canteen,text="  Please select a canteen",borderwidth = 0,font = (None,12))
    l1.pack(side =LEFT)
    listbox = Listbox(frm_canteen_bottom,width = 35,height =6,font = (None,15))

    canteen_list = get_canteen_list(menu)

    for item in canteen_list:
       listbox.insert(END, item)
    a = listbox.bind('<<ListboxSelect>>',lambda x: CurSelet(listbox))
    listbox.pack(padx = 10,side = TOP)
    
    l3 = Button(frm_canteen_bottom,text="GO",width=10, height = 1, command = partial(select_store, menu,frm_canteen,frm_canteen_bottom,a,listbox))
    l3.pack(pady = 5, side = BOTTOM)
   



def select_store(menu,frm_canteen,frm_canteen_bottom,a,listbox1):
    listbox1.unbind('<<ListboxSelect>>', a)
    df_canteen = menu.loc[menu['canteen_name']==canteen]
    frm_canteen.pack_forget()
    frm_canteen_bottom.pack_forget()
    frm_canteen =Frame(root,width = 400,height =200)
    frm_canteen.pack_propagate(0)
    frm_canteen_bottom =Frame(root,width = 400,height =300)
    frm_canteen_bottom.pack_propagate(0)
    frm_canteen.pack()
    frm_canteen_bottom.pack(side = BOTTOM)
    photo1=PhotoImage(file='new_store.png')
    l2 = Label(frm_canteen,image =photo1,borderwidth=0)
    l2.image = photo1
    l2.pack(side=RIGHT,padx=20)
    l1= Label(frm_canteen,text="  Please select a store",borderwidth = 0,font = (None,12))
    l1.pack(side =LEFT)
    listbox = Listbox(frm_canteen_bottom,width = 35,height =6,font = (None,15))

    store_list = get_store_list(df_canteen)
    
    for item in store_list:
       listbox.insert(END, item)
    a = listbox.bind('<<ListboxSelect>>',lambda x:CurSeletStore(listbox))
    listbox.pack(padx = 10,side = TOP)


    
    l3 = Button(frm_canteen_bottom,text="GO",width=10, height = 1, command = partial(show_menu, df_canteen, frm_canteen,frm_canteen_bottom,a,listbox))
    l3.pack(pady = 5, side = BOTTOM)



def show_menu(df_canteen,frm_canteen,frm_canteen_bottom,a,listbox):
    global store, canteen
    listbox.unbind('<<ListboxSelect>>', a)
    df_store = df_canteen.loc[df_canteen['canteen_store']==store]
    frm_canteen.pack_forget()
    frm_canteen_bottom.pack_forget()
    
    canvas=Canvas(root,width=400,height=500,scrollregion=(0,0,1000,5000))
    canvas.place(x = 0, y = 0)

    food_list = show_menu_logic(df_store)

    vertical_pic = 100
    vertical_text = 80
    vertical_price = 130
    
    for item in food_list:
        img_name = item.get('im_name')
        price = item.get('price')
        name = item.get('food')
        img_name = str(img_name)
        price = str(price)
        name = str(name)
        imageee = PhotoImage(file=img_name)
        l1 = Label(canvas,image =imageee,borderwidth=0)
        l1.image = imageee
        l2 = Label(canvas,text =name)
        l3 = Label(canvas,text =price)
        canvas.create_window(100, vertical_pic,window=l1)
        canvas.create_window(300, vertical_text,window=l2)
        canvas.create_window(300, vertical_price,window=l3)
        vertical_pic = vertical_pic + 160
        vertical_text = vertical_text + 160
        vertical_price = vertical_price + 160

    vbar=Scrollbar(canvas,orient=VERTICAL) 
    vbar.place(x = 380,width=20,height=500)
    vbar.configure(command=canvas.yview)
    canvas.config(yscrollcommand=vbar.set)
    b1 =Button(root, text = "BACK", width = 20, height =1, command = select_canteen)
    b1.place(x= 108,y= 450)
    canteen =''
    store = ''


root = Tk()
root.title(" Welcome to SMART CANTEEN ")
root.configure(width=400,height =500)
root_window()
root.mainloop()

