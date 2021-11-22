"""
5th Group Intel for Youth Project:

'Traffic Violation Detection through the use of AI'


Members:
- Carlos Hutahaean
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
import plate_detection

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
        self.allCoorVehicle = []
        self.allCoorPlate = []
        self.choice = ''

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
        file.add_command(label='Refresh', command=self.refresh)
        file.add_separator()
        file.add_command(label='Exit', command=self.leave)
        #violation menu
        violationDetect = Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Violation Detect', menu=violationDetect)
        violationDetect.add_command(label='Draw Line of Interest', command=self.drawLineOfInterestVehicle)
        violationDetect.add_separator()
        violationDetect.add_command(label='Detect Vehicle', command=self.startModelVehicle)
        #plate menu
        plateDetect = Menu(menubar,tearoff=0)
        menubar.add_cascade(label='Plate Detect', menu=plateDetect)
        plateDetect.add_command(label='Draw Line of Interest', command=self.drawLineOfInterestPlate)
        plateDetect.add_separator()
        plateDetect.add_command(label='Detect Plate', command=self.startModelPlate)


##menubar commands
    #edit -> exit
    def leave(self):
        if os.path.exists('images\copy.png'):
            os.remove('images\copy.png')
        exit()

    def refresh(self):
        if os.path.exists('images\pauseframe.png'):
                #define frame
                self.imgSize = Image.open('images\pauseframe.png')
                self.tkimage =  ImageTk.PhotoImage(self.imgSize)
                #output frame
                self.canvas.destroy()
                self.canvas = Canvas(master = root, width = 840, height = 560, cursor='plus')
                self.rec = self.canvas.create_image(0, 0, image=self.tkimage, anchor='nw')
                self.canvas.pack()

    #file -> open
    def openFile(self):
        #locate input
        self.open = filedialog.askopenfilename()
        cap = cv2.VideoCapture(self.open)
        
        try:
            reader = imageio.get_reader(self.open)
            fps = reader.get_meta_data()['fps']
            _, img = cap.read()
            cv2.imwrite('images\preview.png', img)
            self.showImg('images\preview.png')
        except:
            print('An unknown error occured. Please try another input.')

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

    #VD -> draw Line of Interest
    def drawLineOfInterestVehicle(self):
        self.choice = 'vehicle'
        self.canvas.bind('<Button-1>', self.extractCoord)
    
    #PD -> draw Line of Interest
    def drawLineOfInterestPlate(self):
        self.choice = 'plate'
        self.canvas.bind('<Button-1>', self.extractCoord)

    #draw Line of Interest (event)
    def extractCoord(self, event):
        #search if any line has already being made
        try:
            self.clone = cv2.imread('images\copy.png').copy()
        except:
            self.clone = cv2.imread('images\preview.png').copy()

        #first dot
        if self.counter < 1:
            x = int(self.canvas.canvasx(event.x))
            y = int(self.canvas.canvasy(event.y))
            #show mouse click coor
            self.pos.append(self.canvas.create_line(x - 5, y, x + 5, y, fill="red", tags="crosshair"))
            self.pos.append(self.canvas.create_line(x, y - 5, x, y + 5, fill="red", tags="crosshair"))
            self.coor = [(x,y)]
            self.counter += 1

        #second dot
        else:
            x = int(self.canvas.canvasx(event.x))
            y = int(self.canvas.canvasy(event.y))
            #show mouse click coor
            self.pos.append(self.canvas.create_line(x - 5, y, x + 5, y, fill="red", tags="crosshair"))
            self.pos.append(self.canvas.create_line(x, y - 5, x, y + 5, fill="red", tags="crosshair"))
            self.coor.append((x,y))
            self.counter = 0

            if self.choice == 'vehicle':
                #save all (x,y) line to allCoor variable
                self.allCoorVehicle.append(self.coor)
                #draw line
                cv2.line(self.clone, self.coor[0], self.coor[1], (255,0,0), 2)
                cv2.imwrite('images\copy0.png', self.clone)
                self.showImg('images\copy0.png')
            elif self.choice == 'plate':
                #save all (x,y) line to allCoor variable
                self.allCoorPlate.append(self.coor)
                #draw rectangle
                cv2.rectangle(self.clone, self.coor[0], self.coor[1], (0,255,0), 2)
                cv2.imwrite('images\copy1.png', self.clone)
                self.showImg('images\copy1.png')
            self.choice = 0
    

    #VD -> detect Vehicle
    def startModelVehicle(self):
        vehicle_detection.vehicleDetect(self.open, self.allCoorVehicle)

    #PD -> detect Plate
    def startModelPlate(self):
        self.countCar = 0
        self.plate = cv2.imread('images\copy1.png')
        for item in self.allCoorPlate:
            self.copy = self.plate[item[0][1]:item[1][1],item[0][0]:item[1][0]]
            cv2.imwrite('images\car{}.png'.format(self.countCar),self.copy)
            plate_detection.plateDetect('images\car{}.png'.format(self.countCar))
        self.countCar += 1


#declare Widget
root = Tk()
app = Window(root)
root.geometry('535x380')
# root.title(title)       -> dunno why not working :(
root.mainloop()