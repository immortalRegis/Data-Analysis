# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 11:43:46 2024
This to-do list stores it's information in a sqlite database. The UI is designed using tkinter. Any user can
add, modify or delete tasks in the database directly from the application front-end. 
@author: segun
"""

import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import date
import sqlite3 as sql

def query_database():
    conn = sql.connect('Task.db')
    cur = conn.cursor()
    
    query = 'SELECT * FROM list_of_tasks ORDER BY rowid'
    cur.execute(query)
    
    data = cur.fetchall()
    
    for d in data:
        main_tree.insert(parent='', index='end', iid= d[0], values=(d[0],d[1],d[2],d[3],d[4]))
        
        
    
    conn.close()
    
def save_update():
    selected = main_tree.focus()
    main_tree.item(selected, text = '', values = (selected, task_entry.get(), priority.get(), date_created.get(), date_completed.get()))
    
    query = '''
        UPDATE list_of_tasks
        SET 
            task_description = :tsk_desc,
            priority = :pri,
            date_created = :dcr,
            date_completed = :dcm
        WHERE rowid = :selected
    '''
    
    conn = sql.connect('task.db')
    cur = conn.cursor()
    
    cur.execute(query, {'tsk_desc':task_entry.get(), 'pri':priority.get(),
                        'dcr':date_created.get(), 'dcm':date_completed.get(), 'selected':selected})
    conn.commit()
    conn.close()
    clear_entries()
    
    
def delete_record():
    x = main_tree.selection()
    if len(x)> 0:
        rownum = x[0]
        main_tree.delete(x[0])
    
    query = "DELETE FROM list_of_tasks WHERE rowid = :rid"
    
    conn = sql.connect('task.db')
    cur = conn.cursor()  
    cur.execute(query, {'rid':rownum})
    clear_entries()
    conn.commit()
    conn.close()


def select_record(e):
    clear_entries()
    try:
        selected = main_tree.focus()
        values = main_tree.item(selected, 'values')       
        task_entry.insert(0, values[1])
        priority.set(values[2])
        date_created.set_date(values[3])
        date_completed.set_date(values[4])
    except Exception:
        pass


def clear_entries():
    task_entry.delete(0, 'end')
    priority.set('LOW')    
    date_created.set_date(date.today())
    date_completed.set_date(date.today())
    
def add_record():
    task_desc = task_entry.get()
    if len(task_desc.strip()) > 0:
        level = priority.get()
        if len(level.strip()) == 0:
            level = 'LOW'
        assigned = date_created.get()
        completed = date_completed.get()
        
        conn = sql.connect('task.db')
        cur = conn.cursor()
        
        query = '''
            INSERT INTO list_of_tasks (task_description, priority, date_created, date_completed) 
            VALUES(:desc, :level, :created, :completed)
        '''
        cur.execute(query, {'desc': task_desc, 'level': level, 'created':assigned, 'completed':completed})
        conn.commit()
        conn.close()
    
    
    main_tree.delete(*main_tree.get_children())
    query_database()
    clear_entries()
    
    
root = tk.Tk()
root.geometry('600x400')
root.title('To-Do List')

tree_frame = tk.Frame(root)
tree_frame.pack()

conn = sql.connect('task.db')
cur = conn.cursor()
cur.execute('SELECT * FROM list_of_tasks')

column_headings = [row[0] for row in cur.description]

tree_scroll = ttk.Scrollbar(tree_frame)
tree_scroll.pack(side='right', fill='y')

main_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='browse', show= 'headings')
main_tree.pack()
tree_scroll.configure(command=main_tree.yview)

main_tree['columns'] = column_headings

for ch in column_headings:
    main_tree.column(ch, width = 120)
    val = ' '.join(ch.split('_')).title()
    main_tree.heading(ch, text = val )

main_tree.column('#1', width = 25)
main_tree.heading('#1', text='ID')

entry_frame = tk.LabelFrame(root, text='Entries')
entry_frame.pack()

task_label = tk.Label(entry_frame, text='Description')
task_label.grid(row=0, column = 0)

task_entry = tk.Entry(entry_frame, width=25)
task_entry.grid(row=0, column=1)

priority_label = tk.Label(entry_frame, text= 'Priority')
priority_label.grid(row=0, column=2)

priority = ttk.Combobox(entry_frame, state='readonly')
priority['values'] = ['LOW', 'MEDIUM', 'HIGH']
priority.grid(row=0, column = 3)

created_label = tk.Label(entry_frame, text = 'Date Created: ')
created_label.grid(row = 1, column = 0, pady=10)

date_created = DateEntry(entry_frame)
date_created.grid(row = 1, column = 1, pady=10)

completed_label = tk.Label(entry_frame, text = 'Date Completed: ')
completed_label.grid(row = 1, column = 2, pady = 10)

date_completed = DateEntry(entry_frame)
date_completed.grid(row = 1, column = 3, pady=10)

button_frame = tk.LabelFrame(root, text = 'Buttons')
button_frame.pack()

add_button = tk.Button(button_frame, text = 'Add Task', width = 20, command = add_record)
add_button.grid(row = 0 , column = 0, padx = 10, pady = 10)

edit_button = tk.Button(button_frame, text = 'Save Edit', width = 20, command = save_update)
edit_button.grid(row = 0 , column = 1, padx = 10, pady = 10)

del_button = tk.Button(button_frame, text = 'Delete Task', width = 20, command = delete_record)
del_button.grid(row = 0 , column = 2, padx = 10, pady = 10)

main_tree.bind('<ButtonRelease-1>', select_record)
conn.close()
query_database()
root.mainloop()

