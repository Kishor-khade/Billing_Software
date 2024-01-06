from tkinter import *
from tkinter import messagebox, ttk
import os, sys, subprocess
import random
import tempfile
from datetime import date
import pandas as pd



######################################################## functionality part #####################################################
global bill_num
bill_num = random.randint(10000,99999)

if not os.path.exists('bills'):
    os.mkdir('bills')

global data_dict
data_dict = {
    'Name':[], 
    'Phn_Number':[], 
    'Bill_Number':[], 
    'Gold_Rate':[], 
    'GST':[],
    'Date':[], 
    'Product_Name':[], 
    'Product_Weight':[], 
    'Product_Price':[], 
    'Product_Total_Price':[]
}

def re_inititate_dict():
    global data_dict
    data_dict = {
        'Name':[], 
        'Phn_Number':[], 
        'Bill_Number':[], 
        'Gold_Rate':[], 
        'GST':[],
        'Date':[], 
        'Product_Name':[], 
        'Product_Weight':[], 
        'Product_Price':[], 
        'Product_Total_Price':[]
    }


def go_to_next_element(event):
    event.widget.tk_focusNext().focus()


def print_bill():
    if TextArea.get(1.0,END)=='\n':
        messagebox.showerror('Error', 'Bill is empty')
    else:
        file = tempfile.mktemp('.txt')
        open(file,'w').write(TextArea.get(1.0,END))
        if sys.platform == "win32":
            os.startfile(file, 'print')
        else:
            opener = "xdg-open"
            subprocess.call([opener, file])


def search_bill():
    for i in os.listdir('bills/'):
        txt = numberEntry.get()+'_'+billEntry.get()+'.txt'
        if i == txt:
            f = open(os.path.join('bills',i),'r')
            TextArea.delete(1.0,END)
            for data in f:
                TextArea.insert(END, data)
            f.close()
            break
    else:
        messagebox.showerror("Error", "No bill found")


def get_price(weight, qty, price):
    weight = float(weight)
    qty = int(qty)
    price = int(price)
    total = weight*qty*price
    return f"{total:.2f}"


def add_bill_to_dataframe(pName, pWeight, pRate, pTotal):
    data_dict['Name'].append(nameEntry.get())
    data_dict['Phn_Number'].append(numberEntry.get())
    data_dict['Bill_Number'].append(bill_num)
    data_dict['Gold_Rate'].append(goldCurrRate.get())
    data_dict['GST'].append(GstPriceEntry.get())
    data_dict['Date'].append(today)
    data_dict['Product_Name'].append(pName)
    data_dict['Product_Weight'].append(pWeight)
    data_dict['Product_Price'].append(pRate)
    data_dict['Product_Total_Price'].append(pTotal)


def add_product_to_bill(pName, Qty, weight, rate, total):
    pName = ' '+pName
    string = pName.ljust(18)
    TextArea.insert(END, string)
    string = Qty.center(10)
    TextArea.insert(END, string)
    weight = weight+' gm'
    string = weight.center(11)
    TextArea.insert(END, string)
    string = rate.center(10)
    TextArea.insert(END, string)
    string = total.rjust(12)
    TextArea.insert(END, f'{string}\n')


def addPayment():
    if AddPaymentCheckVar.get()==1:
        OnlinePaymentButton['state']='normal'
        CashPaymentButton['state']='normal'
        RemainingBalanceEntry['state']='normal'
        DiscountEntry['state']='normal'
        RemainingBalanceEntry.insert(0,0)
        DiscountEntry.insert(0,0)
    elif AddPaymentCheckVar.get()==0:
        RemainingBalanceEntry.delete(0,END)
        DiscountEntry.delete(0,END)
        OnlinePaymentButton['state']='disabled'
        CashPaymentButton['state']='disabled'
        RemainingBalanceEntry['state']='disabled'
        DiscountEntry['state']='disabled'


def save_bill():
    global bill_num
    phn_num = numberEntry.get()
    result = messagebox.askyesno("Confirm", 'Do you want to save the bill?')
    if result:
        try:
            df = pd.read_csv('bills/database.csv')
        except:
            df = pd.DataFrame(data_dict)
        if itemTotalEntry1.get() not in ['', '0']:
            add_bill_to_dataframe(itemNameEntry1.get(), itemWeightEntry1.get(), itemPriceEntry1.get(), itemTotalEntry1.get())
        if itemTotalEntry2.get() not in ['', '0']:
            add_bill_to_dataframe(itemNameEntry2.get(), itemWeightEntry2.get(), itemPriceEntry2.get(), itemTotalEntry2.get())
        if itemTotalEntry3.get() not in ['', '0']:
            add_bill_to_dataframe(itemNameEntry3.get(), itemWeightEntry3.get(), itemPriceEntry3.get(), itemTotalEntry3.get())
        if itemTotalEntry4.get() not in ['', '0']:
            add_bill_to_dataframe(itemNameEntry4.get(), itemWeightEntry4.get(), itemPriceEntry4.get(), itemTotalEntry4.get())
        if itemTotalEntry5.get() not in ['', '0']:
            add_bill_to_dataframe(itemNameEntry5.get(), itemWeightEntry5.get(), itemPriceEntry5.get(), itemTotalEntry5.get())
        if itemTotalEntry6.get() not in ['', '0']:
            add_bill_to_dataframe(itemNameEntry6.get(), itemWeightEntry6.get(), itemPriceEntry6.get(), itemTotalEntry6.get())
        df = pd.concat([df,pd.DataFrame(data_dict)], ignore_index=True)
        df.to_csv('bills/database.csv', index=None)
        re_inititate_dict()
        bill_content = TextArea.get(1.0, END)
        file = open(os.path.join("bills" ,f"{phn_num}_{bill_num}.txt"), 'w')
        file.write(bill_content)
        file.close()
        messagebox.showinfo("Success", f"Bill number : {bill_num}, is saved successfully")
        bill_num = random.randint(10000,99999)
        messagebox.showinfo("Message", 'Bill Number changed')


def add_payment_to_bill():
    if OnlineCheckVar.get()!=1 and CashCheckVar.get()!=1:
        messagebox.showwarning("Error", "No Payment Mode was selected.\nSo,No payment section added!")
    else:
        TextArea.insert(END, '    Payment Mode      : ')
        if OnlineCheckVar.get()==1 and CashCheckVar.get()==1:
            TextArea.insert(END, 'Online & Cash\n')
        elif OnlineCheckVar.get()==1:
            TextArea.insert(END, 'Online\n')
        else:
            TextArea.insert(END, 'Cash\n')
        remaining = int(RemainingBalanceEntry.get())
        discount = int(DiscountEntry.get())
        paid_amt = totalbill-remaining-discount
        if discount!=0:
            TextArea.insert(END, f'    Discount          : {DiscountEntry.get()}\n')
        TextArea.insert(END, f'    Total Paid amount : Rs.{paid_amt}\n')
        TextArea.insert(END, f'    Remaining amount  : Rs.{remaining}\n')


def clear():
    nameEntry.delete(0,END)
    numberEntry.delete(0,END)
    billEntry.delete(0,END)
    goldCurrRate.delete(0,END)
    silverCurrRate.delete(0,END)
    GstPriceEntry.delete(0,END)
    GstPriceEntry.insert(0,'0')
    itemNameEntry1.delete(0,END);itemNameEntry2.delete(0,END);itemNameEntry3.delete(0,END)
    itemNameEntry4.delete(0,END);itemNameEntry5.delete(0,END);itemNameEntry6.delete(0,END)
    itemWeightEntry1.delete(0,END);itemWeightEntry2.delete(0,END);itemWeightEntry3.delete(0,END)
    itemWeightEntry4.delete(0,END);itemWeightEntry5.delete(0,END);itemWeightEntry6.delete(0,END)
    itemQtyEntry1.delete(0,END);itemQtyEntry2.delete(0,END);itemQtyEntry3.delete(0,END)
    itemQtyEntry4.delete(0,END);itemQtyEntry5.delete(0,END);itemQtyEntry6.delete(0,END)
    itemPriceEntry1.delete(0,END);itemPriceEntry2.delete(0,END);itemPriceEntry3.delete(0,END)
    itemPriceEntry4.delete(0,END);itemPriceEntry5.delete(0,END);itemPriceEntry6.delete(0,END)
    itemTotalEntry1.delete(0,END);itemTotalEntry2.delete(0,END);itemTotalEntry3.delete(0,END)
    itemTotalEntry4.delete(0,END);itemTotalEntry5.delete(0,END);itemTotalEntry6.delete(0,END)
    TextArea.delete(1.0,END)
    AddPaymentCheckVar.set(0)
    OnlineCheckVar.set(0)
    CashCheckVar.set(0)
    DiscountEntry.delete(0,END)
    RemainingBalanceEntry.delete(0,END)
    addPayment()


def total():
    if itemWeightEntry1.get()!='' and itemQtyEntry1.get()!='' and itemPriceEntry1.get()!='':
        total1 = get_price(itemWeightEntry1.get(), itemQtyEntry1.get(), itemPriceEntry1.get())
        itemTotalEntry1.delete(0,END)
        itemTotalEntry1.insert(0, total1)

    if itemWeightEntry2.get()!='' and itemQtyEntry2.get()!='' and itemPriceEntry2.get()!='':
        total2 = get_price(itemWeightEntry2.get(), itemQtyEntry2.get(), itemPriceEntry2.get())
        itemTotalEntry2.delete(0,END)
        itemTotalEntry2.insert(0, total2)
    
    if itemWeightEntry3.get()!='' and itemQtyEntry3.get()!='' and itemPriceEntry3.get()!='':
        total3 = get_price(itemWeightEntry3.get(), itemQtyEntry3.get(), itemPriceEntry3.get())
        itemTotalEntry3.delete(0,END)
        itemTotalEntry3.insert(0, total3)
    
    if itemWeightEntry4.get()!='' and itemQtyEntry4.get()!='' and itemPriceEntry4.get()!='':
        total4 = get_price(itemWeightEntry4.get(), itemQtyEntry4.get(), itemPriceEntry4.get())
        itemTotalEntry4.delete(0,END)
        itemTotalEntry4.insert(0, total4)
    
    if itemWeightEntry5.get()!='' and itemQtyEntry5.get()!='' and itemPriceEntry5.get()!='':
        total5 = get_price(itemWeightEntry5.get(), itemQtyEntry5.get(), itemPriceEntry5.get())
        itemTotalEntry5.delete(0,END)
        itemTotalEntry5.insert(0, total5)
    
    if itemWeightEntry6.get()!='' and itemQtyEntry6.get()!='' and itemPriceEntry6.get()!='':
        total6 = get_price(itemWeightEntry6.get(), itemQtyEntry6.get(), itemPriceEntry6.get())
        itemTotalEntry6.delete(0,END)
        itemTotalEntry6.insert(0, total6)


def bill():
    global totalbill, gst, today
    gst = int(GstPriceEntry.get())
    totalbill=0
    if gst!=0:
        gst = gst/100

    today = date.today()
    today = str(today.strftime("%d/%m/%Y"))
    today_str = "Date : "+today

    if nameEntry.get()=='' or numberEntry.get()=='':
        messagebox.showerror('Error','Customer Details are required')
    elif itemTotalEntry1.get()=='' and itemTotalEntry2.get()=='' and itemTotalEntry3.get()=='' and itemTotalEntry4.get()=='' and itemTotalEntry5.get()=='' and itemTotalEntry6.get()=='':
        messagebox.showerror('Error','Please! \nFind total first')
    elif goldCurrRate.get()=='':
        messagebox.showerror("Error", "Please enter the Live Gold Rate")
    else:
        TextArea.delete(1.0,END)
        TextArea.insert(END, '\n')
        TextArea.insert(END, "Welcome to KK jewellers".center(63))
        TextArea.insert(END, "\n\n")
        TextArea.insert(END, f"Bill Number : {bill_num}".ljust(42))
        TextArea.insert(END, today_str.rjust(20))
        TextArea.insert(END, "\n")
        TextArea.insert(END, f"Customer Name : {nameEntry.get()}".ljust(42))
        TextArea.insert(END, f"Gold Rate : {goldCurrRate.get()}".rjust(20))
        TextArea.insert(END, f"\nCustomer Phone Number : {numberEntry.get()}\n")
        TextArea.insert(END, "\n===============================================================\n")
        TextArea.insert(END, " Product            Quantity    Weight    Rate/gm      Total\n")
        TextArea.insert(END, "===============================================================\n")
        if itemTotalEntry1.get() != '' and itemTotalEntry1.get()!='0':
            totalbill+=float(itemTotalEntry1.get())
            add_product_to_bill(itemNameEntry1.get(),itemQtyEntry1.get(),itemWeightEntry1.get(),itemPriceEntry1.get(),itemTotalEntry1.get())
        if itemTotalEntry2.get() != '' and itemTotalEntry1.get()!='0':
            totalbill+=float(itemTotalEntry2.get())
            add_product_to_bill(itemNameEntry2.get(),itemQtyEntry2.get(),itemWeightEntry2.get(),itemPriceEntry2.get(),itemTotalEntry2.get())
        if itemTotalEntry3.get() != '' and itemTotalEntry1.get()!='0':
            totalbill+=float(itemTotalEntry3.get())
            add_product_to_bill(itemNameEntry3.get(),itemQtyEntry3.get(),itemWeightEntry3.get(),itemPriceEntry3.get(),itemTotalEntry3.get())
        if itemTotalEntry4.get() != '' and itemTotalEntry1.get()!='0':
            totalbill+=float(itemTotalEntry4.get())
            add_product_to_bill(itemNameEntry4.get(),itemQtyEntry4.get(),itemWeightEntry4.get(),itemPriceEntry4.get(),itemTotalEntry4.get())
        if itemTotalEntry5.get() != '' and itemTotalEntry1.get()!='0':
            totalbill+=float(itemTotalEntry5.get())
            add_product_to_bill(itemNameEntry5.get(),itemQtyEntry5.get(),itemWeightEntry5.get(),itemPriceEntry5.get(),itemTotalEntry5.get())
        if itemTotalEntry6.get() != '' and itemTotalEntry1.get()!='0':
            totalbill+=float(itemTotalEntry6.get())
            add_product_to_bill(itemNameEntry6.get(),itemQtyEntry6.get(),itemWeightEntry6.get(),itemPriceEntry6.get(),itemTotalEntry6.get())
        if GstPriceEntry.get()!='0':
            gst = totalbill * gst
            TextArea.insert(END,'---------------------------------------------------------------\n')
            TextArea.insert(END,  "Without GST : ".rjust(50))
            TextArea.insert(END, f"{totalbill:.2f}".rjust(12))
            TextArea.insert(END,'\n')
            TextArea.insert(END, "GST : ".rjust(50))
            TextArea.insert(END, f"{gst:.2f}".rjust(12))
            totalbill += gst
        TextArea.insert(END,'\n---------------------------------------------------------------\n')
        TextArea.insert(END,  "Total Bill : ".rjust(50))
        TextArea.insert(END, f"{totalbill:.2f}".rjust(12))
        TextArea.insert(END,'\n===============================================================\n')
        TextArea.insert(END, '\n')
        if AddPaymentCheckVar.get()==1:
            add_payment_to_bill()

        TextArea.insert(END, '~~~~~~~~~~~~~~ Bill by : kishor-khade.netlify.app ~~~~~~~~~~~~\n')
        # TextArea.insert(END, ' Thank You '.center(63,'*'))
        save_bill()



################################################### GUI part ###########################################################################
root = Tk()
root.title("Billing Software")
root.geometry('1465x865')

# root.iconbitmap(bitmap='icon.png')
# im = Image.open('icon.png')
# photo = ImageTk.PhotoImage(im)
# root.wm_iconphoto(True, photo)



#####################################################  Title part #################################################################
headingLabel = Label(root, text="Billing System",font=('times new roman', 30, 'bold'),bg='darkslateblue',fg='goldenrod1',border=12, relief=GROOVE)
headingLabel.pack(fill=X)



#################3################################  Customer Details part ###########################################################
customer_details_frame = LabelFrame(root, text="Customer Details",font=('times new roman', 20, 'bold'),bg='darkslateblue',fg='goldenrod1',border=8, relief=GROOVE)
customer_details_frame.pack(fill=X)

nameLabel = Label(customer_details_frame,text='Name',font=('times new roman', 15, 'bold'),bg='darkslateblue',fg='white')
nameLabel.grid(row=0, column=0, padx=20)

nameEntry = Entry(customer_details_frame, font=('arial',15), border=7, width=18)
nameEntry.grid(row=0, column=1, padx=8)
nameEntry.bind('<Return>', go_to_next_element)

numberLabel = Label(customer_details_frame,text='Phone Number',font=('times new roman', 15, 'bold'),bg='darkslateblue',fg='white')
numberLabel.grid(row=0,column=2, padx=20,pady=8)

numberEntry = Entry(customer_details_frame, font=('arial',15), border=7, width=18)
numberEntry.grid(row=0, column=3, padx=8)
# numberEntry.bind('<Return>', go_to_next_element)

billLabel = Label(customer_details_frame,text='Bill Number',font=('times new roman', 15, 'bold'),bg='darkslateblue',fg='white')
billLabel.grid(row=0,column=4, padx=20, pady=8)

billEntry = Entry(customer_details_frame, font=('arial',15,'bold'), border=7, width=18)
billEntry.grid(row=0, column=5, padx=8)

searchButton = Button(customer_details_frame, text="SEARCH", command=search_bill, font=('arial',12,'bold'),border=7,width=10)
searchButton.grid(row=0, column=6,padx=20,pady=8)



###3###############################################  Live Rate part ##############################################################
RateFrame = LabelFrame(root, text='Live rate',font=('times new roman', 20, 'bold'),bg='darkslateblue',fg='goldenrod1',border=8, relief=GROOVE)
RateFrame.pack(fill=X)

goldRateLabel = Label(RateFrame,text='Today Gold Rate',font=('times new roman', 15, 'bold'),bg='darkslateblue',fg='white')
goldRateLabel.grid(row=0,column=0, padx=20, pady=8)

goldCurrRate = Entry(RateFrame, font=('arial',15,'bold'), border=7, width=18)
goldCurrRate.grid(row=0, column=1, padx=8,pady=8)
goldCurrRate.bind('<Return>', go_to_next_element)

silverRateLabel = Label(RateFrame,text='Today Silver Rate',font=('times new roman', 15, 'bold'),bg='darkslateblue',fg='white')
silverRateLabel.grid(row=0,column=2, padx=20, pady=8)

silverCurrRate = Entry(RateFrame, font=('arial',15,'bold'), border=7, width=18)
silverCurrRate.grid(row=0, column=3, padx=8, pady=8)
silverCurrRate.bind('<Return>', go_to_next_element)

GstPriceLabel = Label(RateFrame, text='GST % ', font=('times new roman', 15, 'bold'),bg='darkslateblue',fg='white')
GstPriceLabel.grid(row=0, column=4, padx=20, pady=8)

GstPriceEntry = Entry(RateFrame, font=('arial',15), border=7, width=18)
GstPriceEntry.grid(row=0, column=5, padx=8, pady=8)
GstPriceEntry.insert(0,0)
GstPriceEntry.bind('<Return>', go_to_next_element)



##########################3################################  Product  part #############################################################
productFrame = LabelFrame(root, text='Product Details',font=('times new roman', 20, 'bold'),bg='darkslateblue',fg='goldenrod1',border=8, relief=GROOVE)
productFrame.pack(fill=X)


itemAttrCol = Frame(productFrame)
itemAttrCol.grid(row=0,column=0)


IdLabel = Label(productFrame, text='Id',font=('times new roman', 15, 'bold'),bg='darkslateblue',fg='white')
IdLabel.grid(row=0, column=0, padx=10)
NameLabel = Label(productFrame, text='Name ',font=('times new roman', 15, 'bold'),bg='darkslateblue',fg='white')
NameLabel.grid(row=0, column=1, padx=10)
WeightLabel = Label(productFrame, text='Weight (in gm\'s)',font=('times new roman', 15, 'bold'),bg='darkslateblue',fg='white')
WeightLabel.grid(row=0, column=2, padx=10)
QtyLabel = Label(productFrame, text='Quantity',font=('times new roman', 15, 'bold'),bg='darkslateblue',fg='white')
QtyLabel.grid(row=0, column=3, padx=10)
RateLabel = Label(productFrame, text='Rate (per gm)',font=('times new roman', 15, 'bold'),bg='darkslateblue',fg='white')
RateLabel.grid(row=0, column=4, padx=10)
TotalLabel = Label(productFrame, text='Total',font=('times new roman', 15, 'bold'),bg='darkslateblue',fg='white')
TotalLabel.grid(row=0, column=5, padx=10)

options = [ "Mangalsutra", "Earrings", "Bracelet", "Necklace", 
           "Rings", "Chain", "Kada", "Pendant/Lockets", 
           "Bangles/Kangans","Armlet/Bajubandh", "Others"] 


itemNumEntry1 = Label(productFrame, text='1', font=('arial',15, 'bold'), border=5)
itemNumEntry1.grid(row=1,column=0, pady=11, padx=10)
itemNameEntry1 = ttk.Combobox(productFrame, values=options, font=('arial', 15), width=15)
itemNameEntry1.bind('<Return>', go_to_next_element)
itemNameEntry1.grid(row=1,column=1,pady=9, padx=10)
itemWeightEntry1 = Entry(productFrame,font=('arial',15), border=7, width=13)
itemWeightEntry1.bind('<Return>', go_to_next_element)
itemWeightEntry1.grid(row=1,column=2, pady=10, padx=10)
itemQtyEntry1 = Entry(productFrame,font=('arial',15), border=7, width=5)
itemQtyEntry1.bind('<Return>', go_to_next_element)
itemQtyEntry1.grid(row=1,column=3, pady=10, padx=10)
itemPriceEntry1 = Entry(productFrame,font=('arial',15), border=7, width=13)
itemPriceEntry1.bind('<Return>', go_to_next_element)
itemPriceEntry1.grid(row=1,column=4, pady=10, padx=10)
itemTotalEntry1 = Entry(productFrame,font=('arial',15), border=7, width=13)
itemTotalEntry1.bind('<Return>', go_to_next_element)
itemTotalEntry1.grid(row=1,column=5, pady=10, padx=10)


itemNumEntry2 = Label(productFrame, text='2', font=('arial',15, 'bold'), border=5)
itemNumEntry2.grid(row=2,column=0, pady=11, padx=10)
itemNameEntry2 = ttk.Combobox(productFrame, values=options, font=('arial', 15), width=15)
itemNameEntry2.bind('<Return>', go_to_next_element)
itemNameEntry2.grid(row=2,column=1,pady=9, padx=10)
itemWeightEntry2 = Entry(productFrame,font=('arial',15), border=7, width=13)
itemWeightEntry2.bind('<Return>', go_to_next_element)
itemWeightEntry2.grid(row=2,column=2, pady=10, padx=10)
itemQtyEntry2 = Entry(productFrame,font=('arial',15), border=7, width=5)
itemQtyEntry2.bind('<Return>', go_to_next_element)
itemQtyEntry2.grid(row=2,column=3, pady=10, padx=10)
itemPriceEntry2 = Entry(productFrame,font=('arial',15), border=7, width=13)
itemPriceEntry2.bind('<Return>', go_to_next_element)
itemPriceEntry2.grid(row=2,column=4, pady=10, padx=10)
itemTotalEntry2 = Entry(productFrame,font=('arial',15), border=7, width=13)
itemTotalEntry2.bind('<Return>', go_to_next_element)
itemTotalEntry2.grid(row=2,column=5, pady=10, padx=10)


itemNumEntry3 = Label(productFrame, text='3', font=('arial',15, 'bold'), border=5)
itemNumEntry3.grid(row=3,column=0, pady=11, padx=10)
itemNameEntry3 = ttk.Combobox(productFrame, values=options, font=('arial', 15), width=15)
itemNameEntry3.bind('<Return>', go_to_next_element)
itemNameEntry3.grid(row=3,column=1,pady=9, padx=10)
itemWeightEntry3 = Entry(productFrame,font=('arial',15), border=7, width=13)
itemWeightEntry3.bind('<Return>', go_to_next_element)
itemWeightEntry3.grid(row=3,column=2, pady=10, padx=10)
itemQtyEntry3 = Entry(productFrame,font=('arial',15), border=7, width=5)
itemQtyEntry3.bind('<Return>', go_to_next_element)
itemQtyEntry3.grid(row=3,column=3, pady=10, padx=10)
itemPriceEntry3 = Entry(productFrame,font=('arial',15), border=7, width=13)
itemPriceEntry3.bind('<Return>', go_to_next_element)
itemPriceEntry3.grid(row=3,column=4, pady=10, padx=10)
itemTotalEntry3 = Entry(productFrame,font=('arial',15), border=7, width=13)
itemTotalEntry3.bind('<Return>', go_to_next_element)
itemTotalEntry3.grid(row=3,column=5, pady=10, padx=10)


itemNumEntry4 = Label(productFrame, text='4', font=('arial',15, 'bold'), border=5)
itemNumEntry4.grid(row=4,column=0, pady=11, padx=10)
itemNameEntry4 = ttk.Combobox(productFrame, values=options, font=('arial', 15), width=15)
itemNameEntry4.bind('<Return>', go_to_next_element)
itemNameEntry4.grid(row=4,column=1,pady=9, padx=10)
itemWeightEntry4 = Entry(productFrame,font=('arial',15), border=7, width=13)
itemWeightEntry4.bind('<Return>', go_to_next_element)
itemWeightEntry4.grid(row=4,column=2, pady=10, padx=10)
itemQtyEntry4 = Entry(productFrame,font=('arial',15), border=7, width=5)
itemQtyEntry4.bind('<Return>', go_to_next_element)
itemQtyEntry4.grid(row=4,column=3, pady=10, padx=10)
itemPriceEntry4 = Entry(productFrame,font=('arial',15), border=7, width=13)
itemPriceEntry4.bind('<Return>', go_to_next_element)
itemPriceEntry4.grid(row=4,column=4, pady=10, padx=10)
itemTotalEntry4 = Entry(productFrame,font=('arial',15), border=7, width=13)
itemTotalEntry4.bind('<Return>', go_to_next_element)
itemTotalEntry4.grid(row=4,column=5, pady=10, padx=10)


itemNumEntry5 = Label(productFrame, text='5', font=('arial',15, 'bold'), border=5)
itemNumEntry5.grid(row=5,column=0, pady=11, padx=10)
itemNameEntry5 = ttk.Combobox(productFrame, values=options, font=('arial', 15), width=15)
itemNameEntry5.bind('<Return>', go_to_next_element)
itemNameEntry5.grid(row=5,column=1,pady=9, padx=10)
itemWeightEntry5 = Entry(productFrame,font=('arial',15), border=7, width=13)
itemWeightEntry5.bind('<Return>', go_to_next_element)
itemWeightEntry5.grid(row=5,column=2, pady=10, padx=10)
itemQtyEntry5 = Entry(productFrame,font=('arial',15), border=7, width=5)
itemQtyEntry5.bind('<Return>', go_to_next_element)
itemQtyEntry5.grid(row=5,column=3, pady=10, padx=10)
itemPriceEntry5 = Entry(productFrame,font=('arial',15), border=7, width=13)
itemPriceEntry5.bind('<Return>', go_to_next_element)
itemPriceEntry5.grid(row=5,column=4, pady=10, padx=10)
itemTotalEntry5 = Entry(productFrame,font=('arial',15), border=7, width=13)
itemTotalEntry5.bind('<Return>', go_to_next_element)
itemTotalEntry5.grid(row=5,column=5, pady=10, padx=10)


itemNumEntry6 = Label(productFrame, text='6', font=('arial',15, 'bold'), border=5)
itemNumEntry6.grid(row=6,column=0, pady=11, padx=10)
itemNameEntry6 = ttk.Combobox(productFrame, values=options, font=('arial', 15), width=15)
itemNameEntry6.bind('<Return>', go_to_next_element)
itemNameEntry6.config(foreground='black')
itemNameEntry6.grid(row=6,column=1,pady=9, padx=10)
itemWeightEntry6 = Entry(productFrame,font=('arial',15), border=7, width=13)
itemWeightEntry6.bind('<Return>', go_to_next_element)
itemWeightEntry6.grid(row=6,column=2, pady=10, padx=10)
itemQtyEntry6 = Entry(productFrame,font=('arial',15), border=7, width=5)
itemQtyEntry6.bind('<Return>', go_to_next_element)
itemQtyEntry6.grid(row=6,column=3, pady=10, padx=10)
itemPriceEntry6 = Entry(productFrame,font=('arial',15), border=7, width=13)
itemPriceEntry6.bind('<Return>', go_to_next_element)
itemPriceEntry6.grid(row=6,column=4, pady=10, padx=10)
itemTotalEntry6 = Entry(productFrame,font=('arial',15), border=7, width=13)
itemTotalEntry6.bind('<Return>', go_to_next_element)
itemTotalEntry6.grid(row=6,column=5, pady=10, padx=10)



# Bill Total ##############################################3############################
billFrame = Frame(productFrame,border=8,relief=GROOVE)
billFrame.grid(row=0, column=6, padx=10, rowspan=7)

billAreaLabel = Label(billFrame,text='Bill Area', font=('times new roman',15,'bold'), border=7, relief=GROOVE)
billAreaLabel.pack(fill=X)

scrollbar = Scrollbar(billFrame,orient=VERTICAL)
scrollbar.pack(side=RIGHT,fill=Y)

TextArea = Text(billFrame,height=20, width=66, yscrollcommand=scrollbar.set)
TextArea.pack()

scrollbar.config(command=TextArea.yview)



#################################################  Button  part ######################################################################
billMenuFrame = LabelFrame(root, text="Bill Menu", font=('times new roman',20,'bold'), border=7, relief=GROOVE, bg='darkslateblue',fg='goldenrod1')
billMenuFrame.pack(fill=BOTH)




AddPaymentCheckVar = IntVar()
OnlineCheckVar = IntVar()
CashCheckVar = IntVar()
BothCheckVar = IntVar()

PaymentFrame = Frame(billMenuFrame, bg='darkslateblue')
PaymentFrame.grid(row=0,column=0)

AddPaymentButton = Checkbutton(PaymentFrame, text = "Add Payment", variable = AddPaymentCheckVar, 
                            onvalue = 1, offvalue = 0, height = 3, width = 12,
                            command=addPayment, font=('arial', 16, 'bold'))
AddPaymentButton.grid(row=0,column=0, rowspan=2, padx=15)

OnlinePaymentButton = Checkbutton(PaymentFrame, text = "Online", variable = OnlineCheckVar, 
                             onvalue = 1, offvalue = 0, height = 1, width = 12,
                             disabledforeground='white',  
                             font=('arial', 16, 'bold'), bg='darkslateblue', fg='white', 
                             border=5, selectcolor='darkslateblue', state='disabled')
OnlinePaymentButton.grid(row=0,column=1)

CashPaymentButton = Checkbutton(PaymentFrame, text = "Cash", variable = CashCheckVar, 
                             onvalue = 1, offvalue = 0, height = 1, width = 12,
                             disabledforeground='white',  
                             font=('arial', 16, 'bold'), bg='darkslateblue', fg='white', 
                             border=5, selectcolor='darkslateblue', state='disabled')
CashPaymentButton.grid(row=1,column=1)

BalanceFrame = Frame(PaymentFrame, bg='darkslateblue')
BalanceFrame.grid(row=0, column=2, rowspan=2)

RemainingBalanceLabel = Label(BalanceFrame, text='Remaining Balance', font=('arial', 16, ), bg='darkslateblue', fg='white')
RemainingBalanceLabel.grid(row=0,column=0, pady=15, padx=10)

RemainingBalanceEntry = Entry(BalanceFrame, font=('arial', 16, ), bg='white', fg='black', border=5, width=10, state='disabled')
RemainingBalanceEntry.grid(row=0, column=1)

DiscountLabel = Label(BalanceFrame, text="Disount", font=('arial', 16, ), bg='darkslateblue', fg='white')
DiscountLabel.grid(row=1, column=0)
DiscountEntry = Entry(BalanceFrame, font=('arial', 16, ), bg='white', fg='black', border=5, width=10, state='disabled')
DiscountEntry.grid(row=1, column=1)


buttonFrame = Frame(billMenuFrame,border=8, relief=GROOVE, bg='white')
buttonFrame.grid(row=0,column=1, padx=20 )

totalButton = Button(buttonFrame, text='Total', command=total, font=('arial', 16, 'bold'), bg='darkslateblue',fg='white', border=5, width=8, pady=10)
totalButton.grid(row=0,column=0, pady=20, padx=10)

billButton = Button(buttonFrame, text='Bill', command=bill, font=('arial', 16, 'bold'), bg='darkslateblue',fg='white', border=5, width=8, pady=10)
billButton.grid(row=0,column=1, pady=20, padx=10)

printButton = Button(buttonFrame, text='Print', command=print_bill, font=('arial', 16, 'bold'), bg='darkslateblue',fg='white', border=5, width=8, pady=10)
printButton.grid(row=0,column=2, pady=20, padx=10)

clearButton = Button(buttonFrame, text='Clear', command=clear, font=('arial', 16, 'bold'), bg='darkslateblue',fg='white', border=5, width=8, pady=10)
clearButton.grid(row=0,column=3, pady=20, padx=10)



root.mainloop()
