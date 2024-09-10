"""A little helper to improve your vocabulary with Python, Tkinter and SQlite"""

import tkinter.messagebox
from tkinter import *
from tkinter import ttk
import sqlite3

root = Tk()
root.title('Husky Words')


# Create necessary db
with sqlite3.connect('vocabulary.db') as conn:
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS vocabulary(
                word_id INTEGER PRIMARY KEY AUTOINCREMENT,
                ENG TEXT, RUS TEXT
                )""")
    conn.commit()


# Create an add function for the button with connection to db
def add_word():
    word_eng = entry_eng.get(1.0, 'end-1c')
    word_eng = word_eng.capitalize()
    word_rus = entry_rus.get(1.0, 'end-1c')
    word_rus = word_rus.capitalize()
    if word_eng and word_rus:
        print(word_eng)
        print(word_rus)
        with sqlite3.connect('vocabulary.db') as conn:
            cur = conn.cursor()
            cur.execute("""INSERT INTO vocabulary(ENG, RUS) VALUES (?, ?)""", (word_eng, word_rus))
            conn.commit()
            tkinter.messagebox.showinfo('Done', "Added successfully")
            entry_eng.delete(0.0, END)
            entry_rus.delete(0.0, END)

    else:
        tkinter.messagebox.showwarning('Hello Husky', """Please fill in both fields (ENG|RUS)
to add a word to the dictionary""")


# Create show function for the button with connection to db
def show_all():
    show_win = Toplevel(root)
    show_win.title('Vocabulary')
    show_win.geometry('700x300')

    with sqlite3.connect('vocabulary.db') as conn:
        # conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("""SELECT word_id, ENG, RUS FROM vocabulary""")
        rows = cur.fetchall()

        columns = ('ID', 'ENG', 'RUS')
        table = ttk.Treeview(show_win, columns=columns, height=1,
                             selectmode='browse', show='headings')
        table.heading('#1', text='ID')
        table.heading('#2', text='ENG')
        table.heading('#3', text='RUS')
        table.column('ID', width=25)
        table.column('ENG', width=220, anchor=CENTER)
        table.column('RUS', width=220, anchor=CENTER)
        table.rowconfigure(0, weight=1)
        table.columnconfigure(0, weight=1)

        vsb = ttk.Scrollbar(table, orient=VERTICAL, command=table.yview)
        table.pack(fill=BOTH, expand=1)
        vsb.pack(side=RIGHT, fill='y')

        for row in rows:
            table.insert('', END, values=row)


# Create search function for the button with connection to db
def search_word():
    word = entry_search.get()
    word = word.capitalize()
    entry_eng.delete(0.0, END)
    entry_rus.delete(0.0, END)
    if word:
        with sqlite3.connect('vocabulary.db') as conn:

            cur = conn.cursor()
            cur.execute(f"""SELECT * FROM vocabulary WHERE ENG LIKE ? OR RUS LIKE ? OR word_id LIKE ?""",
                        (word, word, word))
            result = cur.fetchall()
            if result:
                for res in result:
                    entry_eng.insert(1.0,
                                     f"""{res[1]}""")
                    entry_rus.insert(1.0, f"""{res[2]}""")
            else:
                tkinter.messagebox.showinfo('No word', 'Not found')

    else:
        tkinter.messagebox.showinfo('Nothing to show', 'Fill in the search box')


# Create update function for the button with connection to db
def update_word():
    word = entry_search.get()
    word = word.capitalize()
    if word:
        with sqlite3.connect('vocabulary.db') as conn:

            cur = conn.cursor()
            cur.execute(f"""SELECT * FROM vocabulary WHERE ENG LIKE ? OR RUS LIKE ?""", (word, word))
            result = cur.fetchall()
            if result:

                edit_win = Toplevel()

                edit_label1 = Label(edit_win, text='OLD ENG:')
                edit_label2 = Label(edit_win, text='OLD RUS:')
                edit_entry1 = Entry(edit_win, width=30)
                edit_entry2 = Entry(edit_win, width=40)
                edit_label1.grid(row=1, column=0)
                edit_entry1.grid(row=1, column=1)
                edit_label2.grid(row=1, column=3)
                edit_entry2.grid(row=1, column=4)

                new_label1 = Label(edit_win, text='NEW ENG:')
                new_entry1 = Entry(edit_win, width=30)
                new_label1.grid(row=2, column=0)
                new_entry1.grid(row=2, column=1)
                new_label2 = Label(edit_win, text='NEW RUS:')
                new_entry2 = Entry(edit_win, width=40)
                new_label2.grid(row=2, column=3)
                new_entry2.grid(row=2, column=4)

                def change_word():
                    new_eng = new_entry1.get()
                    new_eng = new_eng.capitalize()
                    new_rus = new_entry2.get()
                    new_rus = new_rus.capitalize()
                    if new_eng and new_rus:
                        with sqlite3.connect('vocabulary.db') as conn:
                            cur = conn.cursor()
                            cur.execute(f"""UPDATE vocabulary SET ENG=?, RUS=? WHERE word_id={res[0]}""",
                                        (new_eng, new_rus))
                            tkinter.messagebox.showinfo('Update succeeded', 'Done')
                            edit_win.destroy()

                ok = Button(edit_win, text='Save', compound='left', padx=20, command=change_word)
                cancel = Button(edit_win, text='Cancel', anchor='e', padx=20, command=edit_win.destroy)
                ok.grid(row=3, column=0)
                cancel.grid(row=3, column=4)

                for res in result:
                    edit_entry1.insert(0, f"""{res[1]}""")
                    edit_entry2.insert(0, f"""{res[2]}""")
            else:
                tkinter.messagebox.showinfo('Ooopsss!', 'Not found')
    else:
        tkinter.messagebox.showinfo('Nothing to show', 'Fill in the search box')


# Create delete function for the button with connection to db
def delete():
    word = entry_search.get()
    word = word.capitalize()
    if word:
        with sqlite3.connect('vocabulary.db') as conn:

            cur = conn.cursor()
            cur.execute(f"""SELECT * FROM vocabulary WHERE ENG LIKE ? OR RUS LIKE ?""", (word, word))
            result = cur.fetchall()
            if result:
                delete_win = Toplevel()

                delete_label1 = Label(delete_win, text='Delete:')
                delete_entry1 = Entry(delete_win, width=30)
                delete_label1.grid(row=0, column=0)
                delete_entry1.grid(row=0, column=1)

                def delete_word():
                    delete_this = delete_entry1.get()

                    if delete_this:
                        with sqlite3.connect('vocabulary.db') as conn:
                            cur = conn.cursor()
                            cur.execute(f"""DELETE FROM vocabulary WHERE word_id={res[0]}""")
                            tkinter.messagebox.showinfo('Delete succeeded', 'Done')

                            delete_win.destroy()

                ok = Button(delete_win, text='Delete', compound='left', padx=20, command=delete_word)
                cancel = Button(delete_win, text='Cancel', anchor='e', padx=20, command=delete_win.destroy)
                ok.grid(row=3, column=0)
                cancel.grid(row=3, column=4)

                for res in result:
                    delete_entry1.insert(0, f"""{res[1]} {res[2]}""")
            else:
                tkinter.messagebox.showinfo('Ooopsss!', 'Not found')
    else:
        tkinter.messagebox.showinfo('Nothing to show', 'Fill in the search box')


# Create GUI

label_eng = LabelFrame(root, text='Eng')
entry_eng = Text(label_eng, wrap='word')
label_eng.config()
entry_eng.config(width=50, height=10, font=12)

label_rus = LabelFrame(label_eng, text='Rus')
entry_rus = Text(label_rus, wrap='word')
label_rus.config()
entry_rus.config(width=50, height=10, font=12)
label_menu = LabelFrame(label_eng, text='Menu')
entry_search = Entry(label_menu)

but_search = Button(label_menu, text='Search a Word', command=search_word)
but_add = Button(label_menu, text='Add a word to the dictionary', command=add_word)
but_add.config()

but_show_all = Button(label_menu, text='Show all words', command=show_all)
but_show_all.config()

but_update = Button(label_menu, text='Edit record', command=update_word)

but_delete = Button(label_menu, text='Delete a record', command=delete)
but_delete.config()

but_quit = Button(label_menu, text='Quit', command=label_menu.quit)

label_eng.grid(row=1, column=1)
entry_eng.grid(row=2, column=1)
label_rus.grid(row=3, column=1)
entry_rus.grid(row=4, column=1)
label_menu.grid(row=2, column=3)

but_search.grid(row=1, column=1)
entry_search.grid(row=1, column=2)
but_add.grid(row=3, columnspan=3, sticky=EW)
but_show_all.grid(columnspan=3, sticky=EW)
but_update.grid(columnspan=3, sticky=EW)
but_delete.grid(columnspan=3, sticky=EW)
but_quit.grid(row=7, columnspan=3, sticky=EW)

root.mainloop()
