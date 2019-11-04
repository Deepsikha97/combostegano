from tkinter import Tk,filedialog,Frame,BOTH,Button,Label,StringVar,Entry,LEFT,RIGHT,messagebox
from zipfile import ZipFile
import tempfile
from pathlib import Path
import os
from stegano import decode_image
#from ocr import ocr_core
from app import salt,nonce
from encrypt import decrypt

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.file = -1
        self.filename = StringVar()
        self.key = StringVar()
        self.key.set("Not Found!")
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

# textbox
        lbl = Label(self,text="Key")
        lbl.place(x=150, y=250)
        key = Entry(self,bd=5,textvariable=self.key)
        key.place(x=200, y=250)

        file_button = Button(self, text="Decode ! ", command=self.destagano_file)
        # placing the button on my window
        file_button.place(x=200, y=300)
        

    def select_file(self):
        self.file = filedialog.askopenfilename()
        self.filename.set(self.file)
        print(self.file)
    

    def destagano_file(self):
        key = self.key.get()
        print(key)
        if self.file != -1:
            if self.file.endswith(".zip"):
                with ZipFile(self.file,'r') as zip:
                    zip.printdir()
                    dir = tempfile.gettempdir()
                    extract_dir = dir + "\\GUI\\extracted_images\\" + Path(self.file).name[0:-4]
                    #process_dir = dir + "\\GUI\\processed_images\\" + Path(self.file).name[0:-4]
                    print(extract_dir)
                    zip.extractall(extract_dir)
                    # if not os.path.exists(process_dir):
                    #     os.makedirs(process_dir)
                    listfiles = os.listdir(extract_dir)
                    for file in listfiles:
                        msg = decode_image(extract_dir+"\\"+file)
                        print(msg)
                        print("decrypted message : "+decrypt(msg.encode('utf-8'),key,salt,nonce))
                        messagebox.showinfo(file, "decrypted message : "+decrypt(msg.encode('utf-8'),key,salt,nonce))
                    # processedfiles = os.listdir(process_dir)
                    # for file in processedfiles:
                    #     ocr_text = ocr_core(process_dir+"\\"+file)
                    #     print(ocr_text)
                    print("done")



root = Tk()
root.geometry("500x500")
app = Window(root)
root.mainloop()
