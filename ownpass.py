import tkinter
from tkinter import Label, Button, Listbox, Spinbox, simpledialog, Entry, messagebox
from tkinter.constants import RIGHT
import tkinter.font as tkFont
import random
import string
#from PIL import Image, ImageTk
from pykeepass import PyKeePass
import pyperclip as pc

def addPassword():
    length = int(spinLength.get())

    password = "".join(random.sample(string.ascii_letters + string.digits + string.punctuation, length))

    labelPassword['text'] = password

    if "kp" in globals():
        try:
            kp.add_entry(kp.root_group, inputTitle.get(), 'codingschule', password)
            kp.save()
            listboxEntries.insert(listboxEntries.size()+1, inputTitle.get())
        except Exception as error:
            messagebox.showerror("Error", error)

def getPassword(event):
    element = listboxEntries.get(listboxEntries.curselection())
    print(element)
    entry = kp.find_entries(title=element, first=True)
    labelPassword['text'] = entry.password
    pc.copy(entry.password)
    root.after(5000, resetPassword)

def resetPassword():
    labelPassword['text'] = ""

def delete():
    element = listboxEntries.get(listboxEntries.curselection())
    entry = kp.find_entries(title=element, first=True)
    kp.delete_entry(entry)
    kp.save()
    listboxEntries.delete(listboxEntries.curselection())

root = tkinter.Tk()
root.resizable(width=False, height=False)
root.geometry("+2500+400") # Place Window on my second screen

# Schriften definieren
myFont = tkFont.Font(size=20,weight='bold')

root.title("Passwort Generator")
root.iconphoto(False,tkinter.PhotoImage(file='CODING.SCHULE.png'))

#img = Image.open('CODING.SCHULE.png')
#img = img.resize((75,75))
#img = ImageTk.PhotoImage(img)

img = tkinter.PhotoImage(file="CODING.SCHULE.gif")
labelLogo = Label(master=root, image = img)
labelLogo.grid(row=0,column=0,padx=20, pady=10)

labelWelcome = Label(master=root, text="Passwort Generator", fg='#113044', font=myFont)
labelWelcome.grid(row=1,column=0,padx=20, pady=10)

answer = simpledialog.askstring("Passwort Generator", "Bitte das Passwort für die KeePass Datei eingeben!", parent=root, show ='*')

var = tkinter.StringVar(root)
var.set("8")
spinLength = Spinbox(master=root, font=myFont, from_=1, state="readonly", to=20, justify=RIGHT, width=10, textvariable=var)
spinLength.grid(row=2,padx=20, pady=10)

buttonPassword = Button(master=root, bg='#FF5C5C', fg='#FFFFFF', font=myFont, text="Neues Passwort",command=addPassword)
buttonPassword.grid(row=3, column=0, padx=20, pady=10)

labelPassword = Label(master=root, text="", fg='#FF5C5C', font=myFont)
labelPassword.grid(row=4,column=0,padx=20, pady=10)

try:
    kp = PyKeePass('Database.kdbx', password=answer)

    labelTitle = Label(master=root, text="Bezeichnung:", fg='#113044', font=myFont)
    labelTitle.grid(row=5,column=0,padx=20, pady=10, sticky="w")
    inputTitle = Entry(root, font=myFont)
    inputTitle.grid(row=6)
    listboxEntries = Listbox(root,font=myFont)

    labelWelcome['text'] = "Passwort Manager"
    root.title("Simple Passwort Manager")

    for element in kp.entries:
        listboxEntries.insert(listboxEntries.size()+1, element.title)

    listboxEntries.grid(row=7,padx=20,pady=20)
    listboxEntries.bind('<Double-Button-1>', getPassword)

    buttonDelete = Button(master=root, bg='#FF5C5C', fg='#FFFFFF', font=myFont, text="Eintrag löschen",command=delete)
    buttonDelete.grid(row=8, column=0, padx=20, pady=10)

except Exception as error:
    print(error)

root.mainloop()