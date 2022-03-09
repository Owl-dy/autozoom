from tkinter import *
from tkinter import ttk
import os, csv
from utils import *

ws=Tk()

ws.title('Schedule')
ws.geometry('1000x500')

set = ttk.Treeview(ws)
set.pack()

# Setting columns in the table
column_names = ('Meeting Name', 'Meeting Link', 'Date or Day','Start Time', 'End Time')
set['columns']= column_names
set.column("#0", width=0,  stretch=NO)
set.column("Meeting Name",anchor=CENTER, width=80)
set.column("Meeting Link",anchor=CENTER, width=300)
set.column("Date or Day",anchor=CENTER, width=80)
set.column("Start Time",anchor=CENTER, width=80)
set.column("End Time",anchor=CENTER, width=80)

set.heading("#0",text="",anchor=CENTER)
set.heading("Meeting Name",text="Meeting Name",anchor=CENTER)
set.heading("Meeting Link",text="Link",anchor=CENTER)
set.heading("Date or Day",text="Date or Day",anchor=CENTER)
set.heading("Start Time",text="Start Time",anchor=CENTER)
set.heading("End Time",text="End Time",anchor=CENTER)

file_path = os.path.abspath(os.path.dirname(__file__))
csv_path = os.path.join(file_path, 'schedule.csv')
def load_from_csv(set, csv_path):
    """
    read csv and display the content to a table in tkinter treeview
    :param: set a ttk.Treeview() object to specify which set to populate
    """
    
    global line_count
    with open(csv_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0: #to skip the first line in spreadsheet
                    line_count += 1
                else:
                    set.insert(parent='',index='end',iid = line_count-1,text='',values=(row[0], row[1], row[2], row[3], row[4]))
                    line_count += 1

load_from_csv(set, csv_path=csv_path) #load csv from the file and display to the table

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
    """
    get the entries from the entry list and populate the table and write to csv
    """

    # populate table
    global line_count
    global entry_list
    new_entry = [e.get() for e in entry_list]
    set.insert(parent='',index='end',iid = line_count,text='',values=new_entry)
    line_count += 1

    for e in entry_list:
        e.delete(0,END)
   
#Insert New Meeting button
Input_button = Button(ws,text = "Insert New Meeting",command= input_record)
Input_button.pack()

#Select Record
def select_record():
    #clear entry boxes
    global entry_list
    for e in entry_list:
        e.delete(0,END)
    
    #grab record
    global set
    selected=set.focus()
    #grab record values
    values = set.item(selected,'values')

    # change button command to confirm changes
    select_button.configure(text = "Confirm Changes", command=update_record) #once select, change the button command to update_record

    #output to entry boxes
    for i, e in enumerate(entry_list):
        e.insert(0,values[i])

def update_record():
    selected=set.focus()

    #save new data 
    global entry_list
    set.item(selected,text="",values=[e.get() for e in entry_list])
    
   #clear entry boxes
    for e in entry_list:
        e.delete(0,END)
    
    # change button command to select record
    select_button.configure(text = "Edit Highlighted Record", command=select_record) #once update, change the button command to select_record

select_button = Button(ws,text="Edit Highlighted Record", command=select_record)
select_button.pack()

# TODO: Run autozoom button
def parse_all_meetings():
    """ 
    iterate the treeview to get all meetings and create a list of Meeting Object which will be used for autozoom
    :return: List(Meeting Object)
    """
    meeting_list = []
    global ws
    for child in set.get_children():
        row = set.item(child)["values"]
        meeting = Meeting(row[0],row[1], row[2], row[3], row[4], gui_window=ws)
        meeting_list.append(meeting)
    
    return meeting_list

run_button = Button(ws,text="Run AutoZoom!!", command=parse_all_meetings)
run_button.pack()

# Step 2.5: write a function to save treeview to csv / display all from csv (switch back and forward), user can use this function with a button or activate this function when parsing is conpleted
# def save_all_to_csv():
#     # write to csv
#     global csv_path
#     with open(csv_path, 'w', newline='') as file:
#         writer_object = csv.writer(file)
#         for child in set.get_children():
#             row = set.item(child)["values"]
#             entry = [row[0],row[1], row[2], row[3], row[4]]
#             writer_object.writerow(entry)  
#         file.close()

# Step 3: start running the autozoom

# TODO: delete all button

# TODO: visuals for when running autozoom

# for child in set.get_children():
#     print(set.item(child)["values"])

ws.mainloop()