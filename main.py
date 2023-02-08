from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from pytube import YouTube
from pytube import exceptions
from datetime import datetime, timedelta
import winreg

class Youtube_Downloader():
    #initialization and create basic variables
    def __init__(self):
        self.root = Tk() #create tkinter object
        self.root.geometry('600x300') #set dimension of window
        self.root.resizable(height=0,width=0) #window can not enlarge or shrink
        self.root.title("Bunny Video Downloader(Ver0.8)") #set title of window
        self.use_limit = 10 #set use time frequency, default to 10

        #create labels
        Label(self.root,text='Simple Youtube Video Downloader',font='arial 20 bold').pack() #it is the caption of program
        self.link = StringVar() #use to store video link, string type
        Label(self.root,text='Paste Link Here:',font='arial 15 bold').place(x=200,y=60) #indicate users to paste video link here
        self.lingk_enter = Entry(self.root,width=70,textvariable=self.link).place(x=60,y=90)  #create a input field for uers to input
        Label(self.root,text="Program developed by Marlow",font="arial 8").place(x=440,y=265) #developer signature
        Label(self.root,text="Version 0.8",font="arial 8").place(x=470,y=280)

        #check if first time use and set usage time value in Registry
        try:
            reg = winreg.OpenKey(winreg.HKEY_CURRENT_USER,"Software\\Youtube Downloader",
                                reserved=0,access=winreg.KEY_WRITE)
            winreg.CloseKey(reg)
        except Exception:
            messagebox.showinfo(title='Tutorial',
                                message='Please paste the URL of Youtube video in the entry,' 
                                'Parse will analyze the RUL and Download will download video.')
            reg = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER,"Software\\Youtube Downloader",
                                    reserved=0,access=winreg.KEY_WRITE)
            winreg.SetValueEx(reg,'Limits',0,winreg.REG_DWORD,self.use_limit)
            #winreg.SetValueEx(reg,'Reset Code',0,winreg.REG_SZ,os.getlogin()+'00')
            winreg.CloseKey(reg)

        #create two button to operate, 'Parse' button used to analyze the video link and report the info of video,
        #'DOWNLOAD' button used to activate download process
        Button(self.root,text='Parse',font='arial 15 bold',
                bg='azure3',padx=2,
                command=self.Parser,activebackground='cyan').place(x=160,y=130)
        Button(self.root,text='DOWNLOAD',font='arial 15 bold',
                bg='azure3',padx=2,
                command=self.Downloader,activebackground='cyan').place(x=270,y=130)
        
        self.root.mainloop()

    #this function will be activated after pressing 'Parse' button, it will anaylze the video link
    def Parser(self):
        if self.link.get() == '': #if users input nothing in the entry
            messagebox.showwarning(title='Empty Input',message='Plese enter a video link in the input field.')
        else:
            try: #check valid link
                url = YouTube(str(self.link.get())) 
            except exceptions.RegexMatchError: #if the link is not valid address
                messagebox.showwarning(title='Link Error',message='Please enter a valid video link!')
            else:
                video_title = url.title #return the title of video
                video_author = url.author #return the author of video
                video_lenth = str(timedelta(seconds=url.length)) #return the lenth of video
                video_date = datetime.strftime(url.publish_date,'%Y-%m-%d') #return the publish date of video

                #show the info of video
                Label(self.root,text='Video title: '+video_title,font='arial 10').place(x=60,y=180)
                Label(self.root,text='Author: '+video_author,font='arial 10').place(x=60,y=200)
                Label(self.root,text='Publish date: '+video_date,font='arial 10').place(x=60,y=220)
                Label(self.root,text='Video length: '+video_lenth,font='arial 10').place(x=60,y=240)
                
    #this function will be activated after pressing 'DOWNLOAD' button, it will show a resolution choice window,
    #and after choosing desireable resolution, and press 'Begin Download!' button, the download will begin
    def Downloader(self):
        if self.link.get() == '': #if users input nothing in the entry, same as in Parse function
            messagebox.showwarning(title='Empty Input',message='Plese enter a video link in the input field.')
        else:
            try: #check valid link input, same as in Parse function
                url = YouTube(str(self.link.get()))
            except exceptions.RegexMatchError: #if the link is not valid address,same as in Parse function
                messagebox.showwarning(title='Link Error',message='Please enter a valid video link!')
            else:
                try: #check available video link
                    url.check_availability()
                except exceptions.MembersOnly: #if the video is limited, return correspongding warnings
                    messagebox.showwarning(title='Video Error',message='This video is for member-only!')
                except exceptions.RecordingUnavailable:
                    messagebox.showwarning(title='Video Error',message='This video is not availabale!')
                except exceptions.VideoPrivate:
                    messagebox.showwarning(title='Video Error',message='This video is a private video!')
                except exceptions.VideoUnavailable:
                    messagebox.showwarning(title='Video Error',message='This video is not available!')
                else: #if everything is OK......
                    video = url.streams #get steams object
                    #find how many resolutions
                    video_resolution = [] 
                    for stream in video.order_by('resolution'):
                        video_resolution.append(stream.resolution)
                    video_resolutions = list(set(video_resolution))

                    #create resolution choice window for users
                    choice_window = Toplevel()
                    choice_window.geometry('300x150')
                    choice_window.resizable(height=0,width=0)
                    Label(choice_window,text='Resolution Choice',font='arial 15').pack()

                    #create a combobox to choose resolution
                    current_var = StringVar() #string variable
                    choose_resolution = ttk.Combobox(choice_window,textvariable=current_var,values=video_resolutions,state="readonly")
                    choose_resolution.pack()
                
                #a sub-function when user select any resolutions
                def select(event):
                    current_value = current_var.get()
                    choose_resolution.set(current_value)
                
                choose_resolution.bind("<<ComboboxSelected>>",select)

                #a sub-function when user press 'Begin Download!' button
                def begin_download(res): 
                    #read the usage time in registry
                    reg = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER,"Software\\Youtube Downloader",
                                            reserved=0,access=winreg.KEY_ALL_ACCESS)
                    limits = winreg.QueryValueEx(reg,'Limits')
                    num = limits[0]

                    #if usage is not expired, continue to download
                    if num > 0:
                        video.filter(res=res).first().download()
                        num -= 1
                        #if download is compeleted, usage time will reduce 1
                        winreg.SetValueEx(reg,'Limits',0,winreg.REG_DWORD,num)
                        winreg.CloseKey(reg)
                        messagebox.showinfo(title="Download Completed!",
                                            message="Video has been downloaded. Your remaining usage has "+str(num)+".")
                    #if usage is expired, inform users to contact
                    else:
                        messagebox.showwarning(title='Sorry',message='Your usage expired! Please contact developer!')

                #create the button to download
                Button(choice_window,text='Begin Download!',font='arial 10 bold',bg='azure3',command=lambda:begin_download(choose_resolution.get())).pack()           

if __name__ == '__main__':
    FC = Youtube_Downloader()