import tkinter as tk

from tkinter import filedialog, Text, Widget, messagebox
from tkinter.ttk import Progressbar
from tkinter import ttk
from PIL import ImageTk, Image

import os, threading

# pytube
from pytube import YouTube

class TKWindow():

    root = tk.Tk()
    root.title("Mzansi Downloader")
    root.resizable(False, False)
    
    yt = None
    
    # shared resource.
    is_downloading = False

    destination = None
    video_url = None
    url_input = None
    instructionLabel = None
    
    # lock for the shared resource.
    lock = threading.Lock()
    
    def __init__(self):
        
        # create the top menu.    
        menubar = tk.Menu(self.root, bg="black", fg="white")
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu,)
        
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About...", command=self.about_page)
        menubar.add_cascade(label="Help", menu=helpmenu)
        
        self.root.config(menu=menubar)
        
        # canvas
        canvas = tk.Canvas(self.root, height=530, width=450, bg="#000000", )
        canvas.pack()
        
        # frame
        frame = tk.Frame(self.root, bg="white",)
        frame.place(relwidth=0.8, relheight=0.72, relx=0.1, rely=0.1)
        
        # logo 
        diagram = ImageTk.PhotoImage(Image.open("assets/logo.png"))
        logolbl= tk.Label(frame, image = diagram)
        logolbl.image = diagram
        logolbl.pack()
        
        # instruction label
        self.instructionLabel = tk.Label(frame, text="Paste the YouTube link / url below", 
                                    font = ("Helvetica Bold", 15), bg="white")
        self.instructionLabel.pack(padx=10, pady=10)
        
        # textbox
        self.url_input = tk.Text(frame, height = 3, width = 50, 
                                 font=("Helvetica Bold", 15), fg="black",
                                 bg="white",)
        self.url_input.pack(padx=10, pady=10)


        # get directory button
        downloadBtn = tk.Button(frame, text="Download", 
                                    pady=15, padx = 140, fg="white", bg="#263D42",
                                    command=self.start_download_thread)
        downloadBtn.pack()

    # init window
    def startWindow(self):
        self.root.mainloop()

    # Setter: used to set the directory to save the video.
    def setDestination(self):

        self.destination = filedialog.askdirectory()
        
    # Getter: get directory
    def getDestination(self):
        
        if self.destination:
            return self.destination
        else:
            
            # message box
            return None
        
        
    # Setter: set the url / link
    def setVideoURL(self):
        if self.url_input:
            self.video_url = self.url_input.get(1.0, "end-1c")
        else:
            # message box.
            messagebox.showerror("Error: Please insert YouTube link.")
        
    # Getter: get the url / link
    def getVideoURL(self):
        
        if self.video_url:
            return self.video_url
        
        else:
            
            return None
    
    
    # download the video
    def downloadVieo(self):
        self.setDestination()
        self.setVideoURL()
            
        # download the stream.
        try:
            self.yt = YouTube(self.getVideoURL()).streams.first().download(self.getDestination())
            
            messagebox.showinfo(title="Success",message="Media was successfully downloaded.")
            
        except:
            messagebox.showerror(title="Error",message="Error: Could not download.")
            
        self.is_downloading = False
                
        # reset the variables to None
        self.destination = None
        self.video_url = None
        
    # start two threads
    # one for downloading and another for the monitor(Progress bar).
    def start_download_thread(self):
        
        if self.is_downloading == False:
            self.is_downloading = True
            
            progress_monitor_thread  = threading.Thread(target=self.download_monitor_target, daemon= True)
            download_thread = threading.Thread(target=self.downloadVieo, daemon = True)
            
            progress_monitor_thread.start()
            download_thread.start()
            
        else:
            
            messagebox.showwarning(title="Warning",message="Already downloading the media.")


    # monitor thread target function.
    def download_monitor_target(self):
        is_packed = False
        
        downloadFrame = tk.Frame(self.root, bg="#000000",)
        downloadFrame.place(relwidth=1, relheight=1, relx=0.1, rely=0.1)
        downloadFrame.pack(pady = 2)
        
        progress = Progressbar(downloadFrame, style='grey.Horizontal.TProgressbar', 
            length = 100, mode = 'indeterminate')
        progressLabel = tk.Label(downloadFrame, text="Download Progress", 
                                    font = ("Verdana Bold", 15), bg="white", )
        
        while self.is_downloading == True:
            if is_packed == False:
                
                progressLabel.pack(pady = 10, padx = 10)
                progress.pack(padx=10, pady=10)
                is_packed == True
                
            else:
                pass  
            
        progress.pack_forget()
        progressLabel.pack_forget()
        downloadFrame.pack_forget()

    # about page: Display author information and credits.            
    def about_page(self):
        top = tk.Toplevel(self.root)
        top.title("About")
        top.resizable(False, False)
        top.geometry("400x150")
        
        # hardcoded information.
        long_text = """Developer: Richard Zitha \nEmail: equitekconsulting@gmail.com \n\nCredits:\nLogo designer: npktwice\nEmail: thisistwice@gmail.com"""
        
        # create a new frame.
        Aboutframe = ttk.Frame(top)
        Aboutframe.place(relwidth=1, relheight=1, relx = 0.01, rely = 0.01)
        about_info = tk.Label(Aboutframe,text=long_text, font = ("Helvetica Bold", 15), bg="white")
        about_info.pack(pady = 10, padx = 10)
        

    
              
#####################################################################################################################################

if __name__ == "__main__":
    app = TKWindow()
    app.startWindow()