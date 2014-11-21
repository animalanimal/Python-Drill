from tkinter import *
import webbrowser
import sqlite3

conn = sqlite3.connect("c:/Python34/pydrills3.4/dbex3.db")
c = conn.cursor()
root = Tk()

def main():

    root.title('Dept. of Standards and Operations: Orientation and Procedures Division')
    root.geometry('600x400+200+40')

    frame = Frame(root)
    frame.pack(side = BOTTOM)
    
    text = Text(root,
                bg='black',
                fg='#33ff00',
                font='Courier',
                insertbackground='white')
    text.insert('1.0', '(Enter standard operations or orient procedures here.  Or, you know, whatever.)')
    text.pack()


####################


    def listVar():

        # used (by necessity only) for the 'listvariable' in the selBox (listbox) widget

        c.execute("SELECT * FROM mytable")
        conn.commit()
                
    def callSel():

        # calls the popup window, listbox and child textbox,
        # contains a for loop for populating the listbox from dbex3.db

        selWindow = Toplevel(root, bg="black")
        selWindow.title('No one cares')
        selWindow.geometry('600x400+400+240')

        selFrame = Frame(selWindow)
        selFrame.pack(side=LEFT)

        selText=Text(selWindow,
               bg='black',
               fg='#33ff00',
               font='Courier',
               insertbackground='white')
        selText.pack()

        selBox = Listbox(selFrame, listvariable=listVar, height=23, bg='black', fg="#33ff00", selectmode=BROWSE)

        c.execute("SELECT * FROM mytable")
        conn.commit()

        while True:

            row = c.fetchone()
            
            if row is None:
                break
            #print (row)
            selBox.insert(END, row)

        def selMovetext():

            # this object moves the child textbox content to the parent textbox
            
            selGettext = selText.get('1.0','end-1c')
            selTranstext = text.insert('1.0', selGettext)
            selWindow.destroy()

        listButton = Button(selFrame, text='CHOOSE MORTALITY', command=selMovetext)
        listButton.pack(side=BOTTOM)
        
        def selItem(root):

            # this object prints the text from the listbox to the child textbox 

            idxs = selBox.get(first=ACTIVE)
            #print (idxs)
            selText.insert('1.0', idxs)
            
        selBox.bind('<Double-1>', selItem)
        selBox.pack(side=TOP)

        
####################         


    def callSave():

        # saves the parent textbox output to database

        getSavetext = (text.get('1.0', 'end-1c'))
        
        c.execute("INSERT INTO mytable (Field1) VALUES (?)",(getSavetext,))
        conn.commit()

    def callGo():

        # this object controls the passage of text to the html page
        # also contains code for several tkinter buttons
        
        getText = (text.get('1.0', 'end-1c'))
        
        htmlAction = open('StandOp.html','w')

        message = """<html><body bgcolor="black"><font color="#33ff00">
        <title>Dept. of Standards and Operations</title>
        <head><h2><u>Division of Orientation and Procedures</u></h2></head>
        <body><p>%s</p></body>
        </html>""" %(getText)

        htmlAction.write(message)
        htmlAction.close()

        webbrowser.open_new_tab('StandOp.html')

    goButton = Button(frame, text = 'Lozenge your Pitiful Existence',
                                    command = callGo)
    goButton.pack(side=BOTTOM)

    def combineFuncs(*funcs):

        # from stackoverflow, a neat way to add two functions to a button widget
        # used on saveButton
        
        def combinedFunc(*args, **kwargs):

            for f in funcs:
                f(*args, **kwargs)

        return combinedFunc

    saveButton = Button (frame, text = 'Commit to Eternity', command = combineFuncs(callSave, callSel))
    saveButton.pack(side=BOTTOM)

    selButton = Button (frame, text = 'Resurrect Blighted Rejectamenta',
                           command = callSel)
    selButton.pack(side=BOTTOM)


####################


    root.mainloop()

if __name__ == "__main__":
    main()
