from operator import ne
import this
import tkinter as tk
from tkinter import *
import sqlite3
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import time


root = Tk()
root.title("Budgeting app")
canvas = Canvas(root, width = 800, height = 400)

def budget_goal_set():
    conn = sqlite3.connect('budgeting.db') # Connect to or create a new database named 'budgeting.db'
    c = conn.cursor() # Create a cursor object

#Table Creation
    query = "DROP TABLE budget"
    c.execute(query)
    c.execute('''CREATE TABLE IF NOT EXISTS budget(id INTEGER PRIMARY KEY AUTOINCREMENT, amount FLOAT)''')
    query2 = f"INSERT INTO budget (amount) VALUES ({budget_goal_entry_box.get()})"
    c.execute(query2)

    #Saving
    conn.commit() # Save changes to the database
    conn.close()

def budget_goal_set_page():
    for item in canvas.find_all():
        canvas.delete(item)
    return_to_main_menu = Button(root,text = "Return To Main Menu",command=mainpage)
    canvas.create_window(100,50,window =return_to_main_menu)
    budget_goal_label = Label(root,text="Enter a new budegt goal")
    canvas.create_window(100,150,window=budget_goal_label)
    global budget_goal_entry_box
    budget_goal_entry_box = Entry(root,width=20)
    canvas.create_window(100,200,window=budget_goal_entry_box)
    budget_goal_button = Button(root,text="Set Budget",command=budget_goal_set)
    canvas.create_window(100,250,window=budget_goal_button)
    canvas.pack()


#saving the income data to the SQL database
def sql_save_income():
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    conn = sqlite3.connect('budgeting.db') # Connect to or create a new database named 'budget.db'
    c = conn.cursor() # Create a cursor object
    c.execute('''CREATE TABLE IF NOT EXISTS income (id INTEGER PRIMARY KEY AUTOINCREMENT, amount FLOAT, date TEXT,time TEXT)''')
    data = (float(amount_text_box.get()),date,time)
    query = 'INSERT INTO income (amount,date,time) VALUES (?,?,?)'
    c.execute(query,data)
    conn.commit() # Save changes to the database
    conn.close() # Close the connection
    amount_text_box.delete(0,END)

#saving the expenses data to the SQL database
def sql_save_expense():
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    conn = sqlite3.connect('budgeting.db') # Connect to or create a new database named 'budget.db'
    c = conn.cursor() # Create a cursor object
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY AUTOINCREMENT, amount FLOAT, date TEXT,time TEXT)''')
    amount = "-"+amount_text_box.get()
    data = (float(amount),date,time)
    query = 'INSERT INTO expenses (amount,date,time) VALUES (?,?,?)'
    c.execute(query,data)
    conn.commit() # Save changes to the database
    conn.close()
    amount_text_box.delete(0,END)

   



#generating the graphs
def generate_report():
       # Connect to the SQLite database and retrieve the data
    return_to_main_menu = Button(root,text = "Return To Main Menu",command=mainpage)
    canvas.create_window(100,50,window =return_to_main_menu)
    conn = sqlite3.connect("budgeting.db")
    income_query = "SELECT amount, date, time FROM income"
    expense_query = "SELECT amount, date, time FROM expenses"

    income_df = pd.read_sql_query(income_query, conn)
    expense_df = pd.read_sql_query(expense_query, conn)

    # Rename columns to match
    income_df = income_df.rename(columns={'amount': 'income'})
    expense_df = expense_df.rename(columns={'amount': 'expense'})

    # Concatenate income and expense data into a single DataFrame
    merged_df = pd.merge(income_df, expense_df, on=['date','time'], how='outer')

    # Create a bar chart of the data
    merged_df.plot.bar(x='date', y=['income', 'expense'])
    plt.legend(["income", "expense"])
    plt.show()
    canvas.pack()

#income tracking page creation
def track_transaction():
    for item in canvas.find_all():
        canvas.delete(item)
    return_to_main_menu = Button(root,text = "Return To Main Menu",command=mainpage)
    canvas.create_window(100,50,window =return_to_main_menu)
    income_label = Label(root,text="Enter Amount")
    canvas.create_window(230,150,window = income_label)
    global amount_text_box
    amount_text_box = Entry(root,width=20)
    canvas.create_window(230,200,window = amount_text_box)
    income_track_button = Button(root, text = "Track Income", command = sql_save_income)
    canvas.create_window(150,250, window = income_track_button)
    expense_track_button = Button(root, text = "Track Expense", command= sql_save_expense)
    canvas.create_window(300,250, window = expense_track_button)
    canvas.pack()


#Transactions viewing page
def view_transactions():
    for item in canvas.find_all():
        canvas.delete(item)
    conn = sqlite3.connect('budgeting.db') # Connect to or create a new database named 'budgeting.db'
    c = conn.cursor() # Create a cursor object
    return_to_main_menu = Button(root,text = "Return To Main Menu",command=mainpage)
    canvas.create_window(100,50,window =return_to_main_menu)
    # Connect to the SQLite database and retrieve the data
    conn = sqlite3.connect("budgeting.db")
    income_query = "SELECT amount, date, time FROM income"
    expense_query = "SELECT amount, date, time FROM expenses"

    income_df = pd.read_sql_query(income_query, conn)
    expense_df = pd.read_sql_query(expense_query, conn)
    
    # Concatenate income and expense data into a single DataFrame
    global merged_df
    merged_df = pd.concat([income_df, expense_df])

    #sort the dataframe based on date and time
    merged_df.sort_values(by=['date', 'time'], ascending=[False, False],inplace=True)
    sum_of_data = merged_df['amount'].sum()
    sql = "SELECT * FROM budget"
    all = conn.execute(sql)
    for i in all:
        budget = i[1]
    
    if budget == sum_of_data:
        budget_label = Label(root,text=f"You have reached your goal!")
        canvas.create_window(400,50,window=budget_label)
    elif budget<sum_of_data:
        distance_from_goal = sum_of_data-budget
        budget_label = Label(root,text=f"You have reached your goal! You are over by {distance_from_goal}")
        canvas.create_window(400,50,window=budget_label)
    elif budget>sum_of_data:
        distance_from_goal = (budget - (sum_of_data))
        budget_label = Label(root,text=f"You are R{distance_from_goal} away from reaching your goal")
        canvas.create_window(400,50,window=budget_label)



    # Add a scrollbar to the canvas
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    #canvas.create_window(100,150,window = scrollbar)
    scrollbar.pack(side="right",fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame to hold the transactions
    frame = tk.Frame(canvas)
    frame.place(relwidth=1, relheight=1)

    # Add the transactions to the frame
    for i, row in merged_df.iterrows():
        tk.Label(frame, text="amount: {} | Date: {} | Time: {}".format(row["amount"], row["date"], row["time"])).pack()

    # Add the frame to the canvas
    canvas.create_window((50, 100), window=frame, anchor="nw")
    canvas.pack()


#Main Page 
def mainpage():

    for item in canvas.find_all():
        canvas.delete(item)
    View_transaction = Button(root,text = "View Transactions", command= view_transactions)
    canvas.create_window(230,50,window=View_transaction)
    income_button = Button(root, text = "Track Transaction",command = track_transaction)
    canvas.create_window(230,100,window = income_button)
    view_budget = Button(root,text = "View Budget",command = generate_report)
    canvas.create_window(230,150,window = view_budget)
    set_goal_button = Button(root,text = "Set New Goal",command=budget_goal_set_page)
    canvas.create_window(230,200,window=set_goal_button)
    canvas.pack()



mainpage()

root.mainloop()