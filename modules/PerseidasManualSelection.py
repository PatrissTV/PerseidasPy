#Inputs image url
#Opens window to select the meteor
#Returns center of the object and area brightness

from tkinter import *
from PIL import ImageTk,Image,ImageStat
import glob

root = None
screen_width = None
screen_height = None
prop_screen = None

x_factor = None
y_factor = None
frame = None
countRange = 0

x1 = None
y1 = None

crop_x = 0
crop_y = 0

Cx = None
Cy = None
Brightness = None

global_im = None

#Shows zoomed in image to select the object
def selectObj(x1,y1,x2,y2):
    global x_factor
    global y_factor
    global crop_x
    global crop_y
    global global_im


    im=Image.open(frame)
    im=im.crop((x1*x_factor + crop_x, y1*y_factor + crop_y, x2*x_factor + crop_x, y2*y_factor + crop_y))


    crop_x = x1*x_factor + crop_x
    crop_y = y1*y_factor + crop_y
    im = resize(im)
    global_im = im
    root.title("Select meteor")

    for widget in root.winfo_children():
        widget.destroy()

    img_width, img_height = im.size
    canvas = Canvas(root, width = img_width, height = img_height)
    canvas.pack()
    img = ImageTk.PhotoImage(im)
    canvas.create_image(0, 0, anchor=NW, image=img)
    root.bind("<Button-1>", selectRange)
    root.bind("<Button-3>", selectCenter)
    root.mainloop()

#Manages clicks and gets zoom positions
def selectRange(event):
    global countRange
    global x1
    global y1

    if countRange < 1:
        x1 = event.x
        y1 = event.y
        countRange += 1

    elif countRange == 1:
        x2 = event.x
        y2 = event.y
        countRange = 0
        selectObj(x1,y1,x2,y2)

def selectCenter(event):
    global x_factor
    global y_factor
    global crop_x
    global crop_y

    global Cx
    global Cy
    global R
    global G
    global B

    Cx = event.x*x_factor + crop_x
    Cy = event.y*y_factor + crop_y
    print(Cx,Cy)
    R, G, B = calculate_brightness(global_im)
    root.destroy()

def calculate_brightness(image):
    width, height = image.size
    im_r = 0
    im_g = 0
    im_b = 0
    i = 0
    for x in range(width):
        for y in range (height):
            r, g, b = image.getpixel((x, y))

            if(r > 22 and g > 16 and b > 18):
                im_r += r
                im_g += g
                im_b += b
                i += 1
    if i == 0:
        return 0
    else:
        return im_r,im_g,im_b



#Shows image to zoom in
def showImg(im):
    root.title("Zoom In")
    img_width, img_height = im.size
    canvas = Canvas(root, width = img_width, height = img_height)
    canvas.pack()
    img = ImageTk.PhotoImage(im)
    canvas.create_image(0, 0, anchor=NW, image=img)
    root.bind("<Button-1>", selectRange)
    root.mainloop()

#Start function, adjusts image to screen
def resize(im):
    global x_factor
    global y_factor

    img_width, img_height = im.size
    prop_img = img_width/img_height

    #We suppose that the computer screen has proportion > 1
    if prop_img >= prop_screen :
        new_img_width = int(screen_width * 0.8)
        new_img_height = int(screen_width * 0.8/prop_img)
    elif prop_img < prop_screen :
        new_img_height = int(screen_height * 0.8)
        new_img_width = int(screen_height * 0.8 * prop_img)

    x_factor = img_width/new_img_width
    y_factor = img_height/new_img_height

    im = im.resize((new_img_width, new_img_height), Image.ANTIALIAS)
    return im


def start_frame(img):
    global root
    global screen_width
    global screen_height
    global prop_screen

    root = Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    prop_screen = screen_width/screen_height

    global crop_x
    global crop_y

    crop_x = 0
    crop_y = 0

    global frame
    frame = img

    im = Image.open(img)
    im = resize(im)
    showImg(im)

    global Cx
    global Cy
    global R
    global G
    global B

    return Cx, Cy, R, G, B


def init(sample):
    #1
    br1_R = []
    br1_G = []
    br1_B = []
    posX1 = []
    posY1 = []
    count = 0

    for filename in glob.glob('data/samples/'+str(sample)+'.1/*.jpg'):
        print(filename)
        Cx, Cy, R, G, B = start_frame(filename)
        br1_R.append(R)
        br1_G.append(G)
        br1_B.append(B)
        posX1.append(Cx)
        posY1.append(Cy)
        count += 1

    x1 = range(0,count)

    #2
    br2_R = []
    br2_G = []
    br2_B = []
    posX2 = []
    posY2 = []
    count = 0

    for filename in glob.glob('data/samples/'+str(sample)+'.2/*.jpg'):
        Cx, Cy, R, G, B = start_frame(filename)
        br2_R.append(R)
        br2_G.append(G)
        br2_B.append(B)
        posX2.append(Cx)
        posY2.append(Cy)
        count += 1

    x2 = range(0,count)

    return x1,posX1,posY1,br1_R,br1_G,br1_B,x2,posX2,posY2,br2_R,br2_G,br2_B
