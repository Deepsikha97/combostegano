from tkinter import Tk,filedialog,Frame,BOTH,Button,Label,StringVar
from zipfile import ZipFile
import tempfile
from pathlib import Path
import os
from stegano import decode_image
from ocr import ocr_core

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

        file_button = Button(self, text="Decode ! ", command=self.destagano_file)
        # placing the button on my window
        file_button.place(x=200, y=300)
        

    def select_file(self):
        self.file = filedialog.askopenfilename()
        self.filename.set(self.file)
        print(self.file)
    

    def destagano_file(self):
        if self.file != -1:
            if self.file.endswith(".zip"):
                with ZipFile(self.file,'r') as zip:
                    zip.printdir()
                    dir = tempfile.gettempdir()
                    extract_dir = dir + "\\GUI\\extracted_images\\" + Path(self.file).name[0:-4]
                    process_dir = dir + "\GUI\processed_images\\" + Path(self.file).name[0:-4]
                    print(extract_dir)
                    zip.extractall(extract_dir)
                    if not os.path.exists(process_dir):
                        os.makedirs(process_dir)
                    listfiles = os.listdir(extract_dir)
                    for file in listfiles:
                        decode_image(extract_dir+"\\"+file,process_dir+"\\"+file)
                    processedfiles = os.listdir(process_dir)
                    for file in processedfiles:
                        ocr_text = ocr_core(process_dir+"\\"+file)
                        print(ocr_text)
                    print("done")



root = Tk()
root.geometry("500x500")
app = Window(root)
root.mainloop()
