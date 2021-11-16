"""
5th Group Intel for Youth Project:

'Traffic Violation Detection through the use of AI'


Members:
- Carlos Hutahean
- Juan Julio
- Kornelius Hutabarat
- Rijal Gabriel
- Samuel Silaban
- Sean Dorothy
"""

#import libraries
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import imageio
import cv2
import os
#import extensions
import vehicle_detection

#widget
class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.master = master
        self.master.title = 'GUI'
        self.pack(fill=BOTH, expand=1)
        self.counter = 0

        ##var declarations for LoI
        self.pos = []
        self.coor = []
        self.allCoor = []

        ##set start window
        self.fileName = 'images\startup.png'
        self.imgSize = Image.open(self.fileName)
        self.tkimage = ImageTk.PhotoImage(self.imgSize)
        self.canvas = Canvas(master=root, width=535, height=830)
        self.canvas.create_image(0,0, image=self.tkimage, anchor=NW)
        self.canvas.pack()

        ##set menubar
        menubar = Menu(self.master)
        self.master.config(menu=menubar)
        #file menu
        file = Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File', menu=file)
        file.add_command(label='Open', command=self.openFile)
        file.add_separator()
        file.add_command(label='Exit', command=self.leave)
        #edit menu
        edit = Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Edit', menu=edit)
        edit.add_command(label='Draw Line of Interest', command=self.drawLineOfInterest)
        edit.add_separator()
        edit.add_command(label='Detect Vehicle', command=self.startModel)


##menubar commands
    #edit -> exit
    def leave(self):
        if os.path.exists('images\copy.png'):
            os.remove('images\copy.png')
        exit()

    #file -> open
    def openFile(self):
        #locate input
        self.open = filedialog.askopenfilename()
        cap = cv2.VideoCapture(self.open)

        try:
            reader = imageio.get_reader(self.open)
            fps = reader.get_meta_data()['fps']
            _, img = cap.read()
            filename = 'images\preview.png'
            cv2.imwrite(filename, img)
            self.showImg(filename)
        except:
            print('An unknown error occured. Please check your input.')

    #file -> open (show input)
    def showImg(self, filename):
        #resize height = 560
        def resizeImg(filename, height):
            img = cv2.imread(filename)
            dim = None
            (h,w) = img.shape[:2]
            r = height / float(h)
            dim = (int(w*r),height)
            resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
            cv2.imwrite(filename, resized)
            return None
        resizeImg(filename, 560)

        #define frame
        self.imgSize = Image.open(filename)
        self.tkimage =  ImageTk.PhotoImage(self.imgSize)
        #output frame
        self.canvas.destroy()
        self.canvas = Canvas(master = root, width = 840, height = 560, cursor='plus')
        self.rec = self.canvas.create_image(0, 0, image=self.tkimage, anchor='nw')
        self.canvas.pack()

    #edit -> draw Line of Interest
    def drawLineOfInterest(self):
        self.canvas.bind('<Button-1>', self.extractCoord)
        
    #edit -> draw Line of Interest (event)
    def extractCoord(self, event):
        try:
            self.clone = cv2.imread('images\copy.png').copy()
        except:
            self.clone = cv2.imread('images\preview.png').copy()

        if self.counter < 1:
            x = int(self.canvas.canvasx(event.x))
            y = int(self.canvas.canvasy(event.y))
            #show mouse click coor
            self.pos.append(self.canvas.create_line(x - 5, y, x + 5, y, fill="red", tags="crosshair"))
            self.pos.append(self.canvas.create_line(x, y - 5, x, y + 5, fill="red", tags="crosshair"))
            self.coor = [(x,y)]
            self.counter += 1
        else:
            x = int(self.canvas.canvasx(event.x))
            y = int(self.canvas.canvasy(event.y))
            #show mouse click coor
            self.pos.append(self.canvas.create_line(x - 5, y, x + 5, y, fill="red", tags="crosshair"))
            self.pos.append(self.canvas.create_line(x, y - 5, x, y + 5, fill="red", tags="crosshair"))
            self.coor.append((x,y))
            self.counter = 0

            #save all line coor
            self.allCoor.append(self.coor)
            #draw line
            cv2.line(self.clone, self.coor[0], self.coor[1], (255,0,0), 2)
            cv2.imwrite('images\copy.png', self.clone)
            self.showImg('images\copy.png')
    #Detect Vehicle
    def startModel(self):
        vehicle_detection.vehicleDetect(self.open, self.allCoor)


#Declare Widget
root = Tk()
app = Window(root)
root.geometry('535x380')
# root.title(title)

root.mainloop()