from tkinter import *
from tkinter.ttk import *
from tkinter import font, colorchooser, filedialog, messagebox
import os
from title_bar import *

##### ---------------------- Functionality--------------------------------

def clear(event):
    if textarea.get(1.0, END) == "Enter text here...\n":
        textarea.delete(1.0, END)

# View Menu options Functionality :  Tool Bar - Show/Hide
def toolbarFunction():
    if show_toolbar.get() == False:
        tool_bar.pack_forget()
    else:
        textarea.pack_forget()
        tool_bar.pack(fill = X, pady=3, padx=5)
        textarea.pack(fill = BOTH, expand=True, pady=5)


# Status Bar - Show/Hide
def statusbarFunction():
    if show_statusbar.get() == False:
        status_bar.pack_forget()
    else:
        textarea.pack_forget()
        status_bar.pack(side= BOTTOM, pady=3)
        textarea.pack(fill=BOTH, expand=True, pady=5)


### ----------- Find and Replace Window -----------
def find(event=None):

    # Functionality of color theme 
    def window1_color_theme():
        if theme_select == 1:
            dark_title_bar(window1)
        if theme_select == 0:
            light_title_bar(window1)

    # functionality of finding searched word
    def findWord():
        textarea.tag_remove('same',1.0, END)
        start_point = '1.0'
        word=findentryField.get()
        if word:
            while True:
                start_point = textarea.search(word,start_point, stopindex=END)
                if not start_point:
                    break
                end_point = f'{start_point}+{len(word)}c'
                textarea.tag_add('same',start_point,end_point)

                textarea.tag_config('same', foreground='#FFFFFF', background='#5B7EFD')

                start_point = end_point

    
    # functionality of replacing searched word
    def replaceWord():
        word=findentryField.get()
        replacetext = replaceentryField.get()
        data = textarea.get(1.0, END)
        newData = data.replace(word, replacetext)
        textarea.delete(1.0, END)
        textarea.insert(1.0, newData) 
        

    ##### --------------------- SECOND WINDOW STYLING ------------------------------
    window1 = Toplevel()

    window1.title('Find')
    window1.geometry('350x180+500+200')
    window1.resizable(False, False)
    window1.iconphoto(False, img)
    light_title_bar(window1)
        
    window1_color_theme()

    labelFrame = LabelFrame(window1, text= 'Find / Replace')
    labelFrame.pack(pady=20)

    findLabel = Label(labelFrame, text='Find')
    findLabel.grid(row=0, column=0, padx=5, pady=5)
    findentryField = Entry(labelFrame)
    findentryField.grid(row=0, column=1, padx=5, pady=5)

    replaceLabel = Label(labelFrame, text='Replace')
    replaceLabel.grid(row=1, column=0, padx=5, pady=5)
    replaceentryField = Entry(labelFrame)
    replaceentryField.grid(row=1, column=1, padx=5, pady=5)

    findButton = Button(labelFrame, text='FIND', command=findWord)
    findButton.grid(row=2, column=0, padx=3, pady=5)

    replaceButton = Button(labelFrame, text='REPLACE', command=replaceWord)
    replaceButton.grid(row=2, column=1, padx=5, pady=5)

    def doSomething():
        textarea.tag_remove('same', 1.0, END)
        window1.destroy()

    window1.protocol('WM_DELETE_WINDOW', doSomething)
    window1.mainloop()               # ------------- Find and Replace Window End!


# Status Bar Functionality
def statusBarFunction(event):
    if textarea.edit_modified():
        word = len(textarea.get(1.0, END).split())
        characters = len(textarea.get(1.0, 'end-1c').replace(' ', ''))
        status_bar.config(text=f'Characters: {characters}               Words: {word}')
    textarea.edit_modified(False)

# File Menu options Functionality
url = ''


def new_file(event=None):
    global url
    url= ''
    textarea.delete(1.0, END)
    textarea.insert(1.0, "Enter text here...")
    window.title('Text Editor')

def open_file(event=None):
    global url
    url=filedialog.askopenfilename(initialdir = os.getcwd, title = 'Select File', filetypes = (('Text File', 'txt'), ('All Files', '*.*')))
    if url != '':
        textarea.delete(1.0, END)
        data = open(url, 'r')
        textarea.insert(1.0, data.read())
        window.title('Text Editor - '+os.path.basename(url))
    else:
        pass

def save_file(event=None):
    if url == '':
        save_url = filedialog.asksaveasfile(mode='w', defaultextension='.txt', filetypes=(('Text File', 'txt'), ('All Files', '*.*')))
        data = textarea.get(1.0,END)
        if save_url is not None:
            save_url.write(data)
            window.title('Text Editor - '+os.path.basename(save_url.name))
            save_url.close() 
    else:
        data = textarea.get(1.0,END)
        file = open(url, 'w')
        file.write(data)

def saveas_file(event=None):
    save_url = filedialog.asksaveasfile(mode='w', defaultextension='.txt', filetypes=(('Text File', 'txt'), ('All Files', '*.*')))
    data = textarea.get(1.0, END)
    if save_url is not None:
        save_url.write(data)
        window.title('Text Editor - '+os.path.basename(save_url.name))
        save_url.close()
    if url != '':
        os.remove(url)

def exit_file(event=None):
    result = messagebox.askyesnocancel('Warning', 'Do you want to same the file?')
    if result is True:
        if url != '':
            data = textarea.get(1.0,END)
            file = open(url, 'w')
            file.write(data)
            window.destroy()
        else:
            data = textarea.get(1.0, END)
            save_url = filedialog.asksaveasfile(mode='w', defaultextension='.txt', filetypes=(('Text File', 'txt'), ('All Files', '*.*')))
            if save_url is not None:
                save_url.write(data)
                save_url.close()
            window.destroy()
        
    elif result is False:
        window.destroy()
        
    else:
        pass



# Menu Bar options functionality
fontSize = 16
fontStyle = 'Arial'

def font_style(event):
    global fontStyle
    fontStyle = font_family_variable.get()
    myfont.configure(family=fontStyle)

def font_size(event):
    global fontSize
    fontSize = size_variable.get()
    myfont.configure(size=fontSize)

def bold_text():
    if myfont.actual()['weight'] == 'normal':
        myfont.configure(weight='bold')
    else:
        myfont.configure(weight='normal')

def italic_text():
    if myfont.actual()['slant'] == 'roman':
        myfont.configure(slant='italic')
    else:
        myfont.configure(slant='roman')

def underline_text():
    if myfont.actual()['underline'] == 0:
        myfont.configure(underline=1)
    else:
        myfont.configure(underline=0)

def color_text():
    color = colorchooser.askcolor()
    textarea.config(foreground= color[1])

def right_alignment():
    data = textarea.get(1.0, END)
    textarea.tag_config('right', justify=RIGHT)
    textarea.delete(1.0, END)
    textarea.insert(INSERT, data, 'right')

def left_alignment():
    data = textarea.get(1.0, END)
    textarea.tag_config('left', justify=LEFT)
    textarea.delete(1.0, END)
    textarea.insert(INSERT, data, 'left')

def middle_alignment():
    data = textarea.get(1.0, END)
    textarea.tag_config('center', justify=CENTER)
    textarea.delete(1.0, END)
    textarea.insert(INSERT, data, 'center')

def toggleCase():
    data = textarea.get(1.0, END)
    if data.isupper():
        new_data = data.lower()
    else:
        new_data = data.upper()
    textarea.delete(1.0, END)
    textarea.insert(END, new_data)

# Changing Color Themes of Text Editor

def colorThemes(event):
    global theme_select
    theme_select = event
    if theme_select == 0:
        light_title_bar(window)
        window.config(background='#C8E7F2')
        tool_bar.config(background='#C8E7F2')
        filemenu.config(background='#C1DCE4', foreground='#000033')
        viewmenu.config(background='#C1DCE4', foreground='#000033')
        themesmenu.config(background='#C1DCE4', foreground='#000033')
        editmenu.config(background='#C1DCE4', foreground='#000033')
        status_bar.config(background='#C8E7F2', foreground='#000033')
        textarea.config(background='#FFFFFF', foreground='#000033', insertbackground='#000033')

    elif theme_select == 1:
        dark_title_bar(window)
        window.config(background='#343434')
        tool_bar.config(background='#343434')
        filemenu.config(background='#BEBEBE', foreground='#000000')
        viewmenu.config(background='#BEBEBE', foreground='#000000')
        themesmenu.config(background='#BEBEBE', foreground='#000000')
        editmenu.config(background='#BEBEBE', foreground='#000000')
        status_bar.config(background='#343434', foreground='#FFFFFF')
        textarea.config(background='#444444', foreground='#FFFFFF', insertbackground='#FFFFFF')

##### -------------------------------------------- MAIN WINDOW STYLING ------------------------------------------

window = Tk()
window.title("Text Editor")
window.geometry('1100x700+210+15')
window.resizable(False,False)
light_title_bar(window)
img = PhotoImage(file = 'C:\\Users\\91958\\Text_Editor\\images\\icon.png')
window.iconphoto(False,img)

# Menu Bar
menubar = Menu(window)
window.config(menu=menubar, background='#C8E7F2')

# File Menu Section
newFileImage = PhotoImage(file='images/newFile.png')
openFileImage = PhotoImage(file='images/openFile.png')
saveFileImage = PhotoImage(file='images/saveFile.png')
saveAsFileImage = PhotoImage(file='images/saveAsFile.png')
exitFileImage = PhotoImage(file='images/exitFile.png')

filemenu = Menu(menubar, tearoff=False, background='#C1DCE4', foreground='#000033')
menubar.add_cascade(label='File', menu=filemenu)

filemenu.add_command(label='New File', accelerator = "Ctrl+N", image = newFileImage, compound= LEFT, command = new_file)
filemenu.add_command(label='Open File', accelerator = "Ctrl+O", image = openFileImage, compound= LEFT, command = open_file)
filemenu.add_command(label='Save', accelerator = "Ctrl+S", image = saveFileImage, compound= LEFT, command = save_file)
filemenu.add_command(label='Save As', accelerator = "Ctrl+R", image = saveAsFileImage, compound= LEFT, command = saveas_file)
filemenu.add_separator()
filemenu.add_command(label='Exit', accelerator = "Ctrl+Q", image = exitFileImage, compound= LEFT, command = exit_file)


# Edit Menu Section
cutImage = PhotoImage(file='images/cut.png')
copyImage = PhotoImage(file='images/copy.png')
pasteImage = PhotoImage(file='images/paste.png')
clearImage = PhotoImage(file='images/clear.png')
findImage = PhotoImage(file='images/find.png')
selectAllImage = PhotoImage(file='images/selectall.png')

editmenu = Menu(menubar, tearoff=False, background='#C1DCE4', foreground='#000033')
menubar.add_cascade(label='Edit', menu=editmenu)

editmenu.add_command(label='Cut', accelerator = "Ctrl+X", image = cutImage, compound= LEFT, command=lambda : textarea.event_generate('<Control x>'))
editmenu.add_command(label='Copy', accelerator = "Ctrl+C", image = copyImage, compound= LEFT, command=lambda : textarea.event_generate('<Control c>'))
editmenu.add_command(label='Paste', accelerator = "Ctrl+V", image=pasteImage, compound=LEFT, command=lambda: textarea.event_generate('<Control v>'))
editmenu.add_command(label='Select All', accelerator = "Ctrl+A", image=selectAllImage, compound=LEFT)
editmenu.add_command(label='Clear', image = clearImage, compound= LEFT, command = lambda : textarea.delete(1.0, END))
editmenu.add_command(label='Find', accelerator = "Ctrl+F", image = findImage, compound= LEFT, command = find)


# View Menu Section
show_toolbar = BooleanVar()
show_statusbar = BooleanVar()

toolBarImage = PhotoImage(file='images/toolbar.png')
statusBarImage = PhotoImage(file='images/statusbar.png')

viewmenu = Menu(menubar, tearoff=False, background='#C1DCE4', foreground='#000033')
menubar.add_cascade(label='View', menu=viewmenu)

viewmenu.add_checkbutton(label='Tool Bar     ', variable= show_toolbar, onvalue=True, offvalue=False, image= toolBarImage, compound= RIGHT, command= toolbarFunction)

show_toolbar.set(True)

viewmenu.add_checkbutton(label='Status Bar  ', variable=show_statusbar, onvalue=True, offvalue=False, image=statusBarImage, compound=RIGHT, command=statusbarFunction)

show_statusbar.set(True)


# Theme Menu Section
lightImage = PhotoImage(file = 'images/light.png')
darkImage = PhotoImage(file = 'images/dark.png')

themesmenu = Menu(menubar, tearoff=False, background='#C1DCE4', foreground='#000033')
menubar.add_cascade(label='Themes', menu=themesmenu)
theme_select = IntVar()

themesmenu.add_radiobutton(label='Light   ', image = lightImage, value=0, variable = theme_select, compound = RIGHT, command = lambda:colorThemes(0))
themesmenu.add_radiobutton(label='Dark    ', image = darkImage, value=1, variable = theme_select, compound = RIGHT, command = lambda : colorThemes(1))


# Tool Bar Section
tool_bar = Label(window, background='#C8E7F2')
tool_bar.pack(side = TOP, fill = X, pady=10, padx=5)

## Font-Style Section
font_families = font.families()
font_family_variable = StringVar()

fontfamily_Combobox = Combobox(tool_bar, width = 30, values = font_families, state = 'readonly', textvariable = font_family_variable)
fontfamily_Combobox.current(font_families.index('Arial'))
fontfamily_Combobox.grid(row=0, column=0, padx = 5)

fontfamily_Combobox.bind('<<ComboboxSelected>>', font_style)

## Font-Size Section
size_variable = IntVar()

font_size_Combobox = Combobox(tool_bar, width = 6, textvariable = size_variable, values = tuple(range(8,81,2)), state = 'readonly')
font_size_Combobox.current(4)  # size - 16
font_size_Combobox.grid(row=0, column=1, padx=5)

font_size_Combobox.bind('<<ComboboxSelected>>', font_size)

myfont = font.Font(family=fontStyle, size=fontSize)

## Button Section

boldImage = PhotoImage(file = 'images/bold.png')
boldButton = Button(tool_bar, image=boldImage, command=bold_text)
boldButton.grid(row=0, column=2)

italicImage = PhotoImage(file = 'images/italic.png')
italicButton = Button(tool_bar, image=italicImage, command= italic_text)
italicButton.grid(row=0, column=3)

underlineImage = PhotoImage(file = 'images/underline.png')
underlineButton = Button(tool_bar, image=underlineImage, command=underline_text)
underlineButton.grid(row=0, column=4)

colorWheelImage = PhotoImage(file = 'images/colorWheel.png')
colorWheelButton = Button(tool_bar, image=colorWheelImage, command=color_text)
colorWheelButton.grid(row=0, column=5, padx = 5)

leftImage = PhotoImage(file = 'images/left.png')
leftButton = Button(tool_bar, image=leftImage, command= left_alignment)
leftButton.grid(row=0, column=6)

middleImage = PhotoImage(file = 'images/middle.png')
middleButton = Button(tool_bar, image=middleImage, command=middle_alignment)
middleButton.grid(row=0, column=7)

rightImage = PhotoImage(file = 'images/right.png')
rightButton = Button(tool_bar, image=rightImage, command=right_alignment)
rightButton.grid(row=0, column=8)

caseImage = PhotoImage(file = 'images/case.png')
caseButton = Button(tool_bar, image=caseImage, command=toggleCase)
caseButton.grid(row=0, column=9, padx=5)

# Scroll Bar Section
scrollbar = Scrollbar(window)
scrollbar.pack(side=RIGHT, fill=Y)

# Status Bar Section
status_bar = Label(window, text='Status Bar', font=('arial', 10), background='#C8E7F2', foreground='#000033')
status_bar.pack(side=BOTTOM, pady=3)

# Text Area Section
textarea = Text(window, yscrollcommand=scrollbar.set, font=("arial", 16), padx=10, pady=10, background='#FFFFFF', foreground='#000033', insertbackground='#000033', undo=True)
textarea.pack_propagate(False)
textarea.pack(fill = BOTH, expand = True)
textarea.insert(1.0, "Enter text here...")
textarea.config(font=myfont)

scrollbar.config(command = textarea.yview)

textarea.bind("<Button-1>", clear)
textarea.bind("<Key>", clear)
textarea.bind('<<Modified>>', statusBarFunction)

window.bind('<Control-o>',open_file)
window.bind('<Control-n>',new_file)
window.bind('<Control-s>',save_file)
window.bind('<Control-r>',saveas_file)
window.bind('<Control-q>',exit_file)

window.bind('<Control-f>',find)

window.mainloop()