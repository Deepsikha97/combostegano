from tkinter import Tk,filedialog,Frame,BOTH,Button,Label,StringVar

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.file = -1
        self.filename = StringVar()
        self.filename.set("No File Selected!")
        self.init_window()

    def init_window(self):
        # changing the title of our master widget
        self.master.title("GUI")
        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)
        # creating a button instance
        file_button = Button(self, text="Select File ! ", command=self.select_file)
        # placing the button on my window
        file_button.place(x=200, y=200)
        text = Label(self, textvariable=self.filename)
        text.pack(fill="x")

    def select_file(self):
        self.file = filedialog.askopenfilename()
        self.filename.set(self.file)
        print(self.file)

root = Tk()
root.geometry("500x500")
app = Window(root)
root.mainloop()
