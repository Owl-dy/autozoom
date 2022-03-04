from tkinter import *
from tkinter import ttk
import os, csv

ws=Tk()

ws.title('Schedule')
ws.geometry('800x300')

set = ttk.Treeview(ws)
set.pack()

# Setting columns in the table
column_names = ('Meeting Name', 'Meeting Link', 'Date','Time')
set['columns']= column_names
set.column("#0", width=0,  stretch=NO)
set.column("Meeting Name",anchor=CENTER, width=80)
set.column("Meeting Link",anchor=CENTER, width=300)
set.column("Date",anchor=CENTER, width=80)
set.column("Time",anchor=CENTER, width=80)

set.heading("#0",text="",anchor=CENTER)
set.heading("Meeting Name",text="Meeting Name",anchor=CENTER)
set.heading("Meeting Link",text="Link",anchor=CENTER)
set.heading("Date",text="Date",anchor=CENTER)
set.heading("Time",text="Time",anchor=CENTER)


def load_from_csv(set):
    """
    read csv and display the content to a table in tkinter treeview
    :param: set a ttk.Treeview() object to specify which set to populate
    """
    file_path = os.path.abspath(os.path.dirname(__file__))
    csv_path = os.path.join(file_path, 'schedule.csv')
    global line_count
    with open(csv_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0: #to skip the first line in spreadsheet
                    line_count += 1
                else:
                    line_count += 1
                    set.insert(parent='',index='end',iid = line_count-1,text='',values=(row[0], row[1], row[2], row[3], row[4]))

load_from_csv(set) #load csv from the file and display to the table

Input_frame = Frame(ws)
Input_frame.pack()


def create_entry_field(Input_frame, column_names):
    entry_list = []
    for i,col in enumerate(column_names):
        l = Label(Input_frame,text=col)
        l.grid(row=0,column=i)
        e = Entry(Input_frame)
        e.grid(row=1,column = i)
        entry_list.append(e)
    return entry_list

entry_list = create_entry_field(Input_frame=Input_frame, column_names=column_names)

def input_record():
    

    global line_count
    global entry_list
    set.insert(parent='',index='end',iid = line_count,text='',values=[e.get() for e in entry_list])
    line_count += 1

    for e in entry_list:
        e.delete(0,END)
   
     
#button
Input_button = Button(ws,text = "Insert New Meeting",command= input_record)

Input_button.pack()



ws.mainloop()