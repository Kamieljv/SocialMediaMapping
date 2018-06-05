"""
Modified on Tue 5 Jun 2018
@author: Kamieljv (GitHub)
labeling_tool.py:
    label a set of satellite images manually
    sampling possible
    importing labels possible (csv or pickle)
Instructions:
    The script will open a window that displays an image. Browsing through the images can be done
    with the left/right arrow keys. The label of the image is displayed next to the filename above the
    image. The label 'XXX' represents an unlabeled image. The keys 'r' and 'n' classify the images as
    'contains roads/buildings' and 'does not contain roads/buildings', respectively.
    Terminating the script automatically saves the progress to a pickle file (with date and time), which
    can be loaded later.
"""

import os
from PIL import Image, ImageTk
import tkinter as tk
import pickle
import time
import csv

def get_rev_images(input, filename):
    if input:
        lbl_lst = process_input(input, filename)
    else:
        lbl_lst = [-1 for c in 'c' * len(image_lst)]
    return lbl_lst

def process_input(type, filename):
    if type=="csv":
        data = []
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for line in reader:
                data.append(line[6])
            data = data[1:]
            lbl_lst = [1 if float(tile)>0 else -1 for tile in data]
        return lbl_lst
    elif type=="pickle":
        objects = dict()
        with open(filename, 'rb') as f:
            try:
                while True:
                    objects.update(pickle.load(f))
            except Exception:
                pass
        return objects[image_dir]

def no_road(e):
    global Release, i
    if Release:
        print('Im_nr: {}    '.format(i)+'no road'+ '\t'+image_lst[i])
        lbl_lst[i]=0
        Release = False
        next_image(e)

def road(e):
    global Release, i
    if Release:
        print('Im_nr: {}    '.format(i)+'road'+ '\t'+image_lst[i])
        lbl_lst[i]=1
        Release = False
        next_image(e)

def next_image(e):
    global img, i
    print(i)
    i+=1 + skip
    if i >= len(image_lst):
        root.destroy()
    # elif lbl_lst[i]==1:
    #     next_image(None)
    else:
        img2 = ImageTk.PhotoImage(Image.open(image_dir+image_lst[i]).resize((width,height)))
        panel.configure(image=img2)
        panel.image = img2
        name.configure(text=image_lst[i]+' - '+transl[lbl_lst[i]])
        img = img2

def prev_image(e):
    global img, i
    i-=1 + skip
    img2 = ImageTk.PhotoImage(Image.open(image_dir+image_lst[i]).resize((width,height)))
    panel.configure(image=img2)
    panel.image = img2
    name.configure(text=image_lst[i]+' - '+transl[lbl_lst[i]])
    img = img2

def release(e):
    global Release
    Release = True


#Initialize image structures
image_dir = ''
image_lst = os.listdir(image_dir)
transl = {-1:"XXX", 0:"no roads", 1:"roads"}
skip = 0 #set the number of cells that are skipped in iteration

#Getting list of labels
csv_file = ''
lbl_lst = get_rev_images("csv", csv_file) #change argument to True if input file is given

#Initializing Image viewer
root = tk.Tk()
i = 0
width = 600 #width of displayed image
height = 600 #height of displayed image
img = ImageTk.PhotoImage(Image.open(image_dir+image_lst[i]).resize((width,height)))
panel = tk.Label(root, image=img)
panel.pack(side="bottom", fill="both", expand="yes")
name = tk.Label(root, text=image_lst[i]+' - '+transl[lbl_lst[i]])
name.pack(side="top")

#Defining Keys and Release Checks
Release = True
root.bind("<KeyRelease-r>", release)
root.bind("<KeyRelease-n>", release)
root.bind("r", road)
root.bind("n", no_road)
root.bind("<Left>", prev_image)
root.bind("<Right>", next_image)

root.mainloop()

#Saving label list as pickle file
dictio = {image_dir: lbl_lst, "reviewed_nr":i+1}
today = time.strftime("%Y%m%d-%H%M%S")
filebase = '' #a base-name of the file (make it end with _)
pickle.dump(dictio, open(filebase+today+'.p', 'wb'))

