from tkinter import *
from tkinter import messagebox
import tkinter
import winreg

class YoutubeDownloaderReset():
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry('400x140') #set dimension of window
        self.root.resizable(height=0,width=0) #window can not enlarge or shrink
        self.root.title("Youtube Downlader Reset")

        Label(self.root,text='Youtube Downloader Reset(Ver1.0)',font='arial 20 bold').pack()
        Button(self.root,text='Reset',font='arial 15 bold',
               bg='azure3',padx=2,command=self.Reset).place(x=160,y=60)
        
        self.root.mainloop()

    def Reset(self):
        reg = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER,"Software\\Youtube Downloader",
                               reserved=0,access=winreg.KEY_WRITE)
        winreg.SetValueEx(reg,'Limits',0,winreg.REG_DWORD,10)
        winreg.CloseKey(reg)
        messagebox.showinfo(title="Reset completed!",
                            message="Reset completed! Now you have 10 usages to download video.")
        #print("work")

if __name__ == '__main__':
    FC = YoutubeDownloaderReset()