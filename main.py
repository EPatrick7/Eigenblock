import numpy as np
from PIL import Image,ImageTk
import tkinter as tk
from tkinter import Entry,Button, Frame, Scrollbar, messagebox,Scale
import matplotlib.pyplot as plt
import os
from math import sqrt
import glob
plt.rcParams['toolbar'] = 'None'

max_images=5000

n=250
texture_folder="lfw-deepfunneled"
current_format="jpg"
base_block="Aaron_Eckhart\Aaron_Eckhart_0001"
base_block2="George_W_Bush\George_W_Bush_0001"


#n=100
#texture_folder="faces"
#current_format="jpg"
#base_block="001_03"
#base_block2="002_03"


#n=16
#texture_folder="textures"
#current_format="png"

#base_block="dirt"
#base_block2="diamond_block"

global brightness_offset
brightness_offset=0



def output_plot(matrix):
    '''Renders a matrix as a matplot plot'''
    matrix+=np.ones_like(matrix)*brightness_offset
    
    plt.figure("EigenBlock Construction")
    plt.imshow(matrix, cmap='gray', vmin=0, vmax=255)
    plt.axis('off')
    plt.show()

def plot_vector(vector):
    '''Unpacks a n^2 Vector into a nxn matrix and plots it'''
    vector=np.transpose(vector)
    output_plot(vector.reshape(n,n))

def output_image(matrix):
    '''Outputs a matrix as a standard image file'''
    matrix_normalized = (matrix * (n*n)).astype(np.uint8)
    image = Image.fromarray(matrix_normalized, mode='L')
    image.show()

def read_texture(file_path):
    '''Reads a single texture and returns it as a vector.'''
    image = Image.open(file_path)
    image_gray = image.convert('RGBA').convert('L')
    matrix = np.array(image_gray)
    return np.transpose(matrix.flatten())

          
            
def read_textures():
    '''Inputs all files of nxn into a matrix in mean-deviation form'''
    textures = glob.glob(os.path.join(texture_folder+"/", '*.'+current_format), recursive=True)
    all_textures=[]
    #print("Loading Images...")
    i=0
    for root, _, files in os.walk(texture_folder):
        if i >=max_images:
            break
        for file_name in files:
            if i >=max_images:
                break
            file_path = os.path.join(root, file_name)
            print(file_path)
            if file_name.endswith('.' + current_format):
                image = Image.open(file_path)
                if image.size == (n, n): # Throw out all images not of size nxn.
                    image_gray = image.convert('RGBA').convert('L')
                    matrix = np.array(image_gray)
                    i+=1
                    all_textures.append(matrix.flatten())
    if len(all_textures)<=0:
        raise ValueError("There were no files found that fit " +texture_folder +"/*."+current_format)
    all_textures=np.vstack(all_textures)
    print("Performing SVD...")
    row_means = np.mean(all_textures, axis=1, keepdims=True)
    
    return all_textures - row_means,row_means
def round_out(matrix):
    '''Rounds all values really close to 0 to 0'''
    rounder = lambda val: 0 if abs(val) < 1e-2 else val
    if matrix.ndim == 1: #If vector
        return np.array([rounder(i) for i in matrix])
    else: #If Matrix
        return np.array([[rounder(i) for i in row] for row in matrix])
def coef_to_vector(w,Vh):
    '''Turns w back into its image matrix'''
    return np.transpose(Vh)@w

#Get all textures and then compress each one into a row in a giant matrix
all_textures,row_means=read_textures()

global w,Vh,w_last

#Perform singular value decomposition on the matrix
U,Svals,Vh=np.linalg.svd(all_textures, full_matrices=False)
S=np.diag(Svals)
#all_textures = U @ S @ Vh

w_last=None

def read_block():
    '''Updates w to the current base_block id'''
    global w,w_last
    w_last=None
    w= Vh@(read_texture(texture_folder+"/"+base_block+"."+current_format))
    return w

read_block()
#plot_vector(coef_to_vector(w,Vh))



#TKINTER:


root = tk.Tk()
root.title("Eigenblocks")
root.geometry("1200x500")

frame = Frame(root)
frame.pack(side=tk.TOP, fill=tk.BOTH,expand=True)

scrollbar = Scrollbar(frame, orient=tk.HORIZONTAL)
scrollbar.pack(side=tk.BOTTOM, fill=tk.BOTH)


scrollbar2 = Scrollbar(frame, orient=tk.VERTICAL)
scrollbar2.pack(side=tk.LEFT, fill=tk.BOTH)

canvas = tk.Canvas(frame, bd=0, highlightthickness=0, xscrollcommand=scrollbar.set,yscrollcommand=scrollbar2.set)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=canvas.xview)
scrollbar2.config(command=canvas.yview)

inner_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=inner_frame, anchor=tk.NW)
def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox('all'))
inner_frame.bind('<Configure>', on_configure)

num_rows = round(sqrt(w.size))
num_cols = w.size/num_rows
if num_cols != round(num_cols):
    num_cols=int(num_cols)+1
num_cols=int(num_cols)

print("Setting Up Tkinter: "+str(num_rows)+"x"+str(num_cols))


w_entries = []

sv=round_out(Svals)


def update_brightness(event):
    global brightness_offset
    brightness_offset=float(brightness_block.get())

def update_plot(event):
    plot_reconstructed_texture()


for i in range(num_rows):
    row_entries = []
    for j in range(num_cols):
        if i*num_cols+j>=w.size:
            break
        entry = Entry(inner_frame, width=10)
        val=round(w[i * num_cols + j],2)
        
       # if sv[i * num_cols + j] ==0: #If this dimension is not needed....
       #     val=0 
        
        entry.insert(0,str(val))
        entry.grid(row=i, column=j, padx=5, pady=5)
        entry.bind('<KeyRelease>', update_plot)
        row_entries.append(entry)
    if i*num_cols+j>=w.size:
        break
    w_entries.append(row_entries)
    



def plot_reconstructed_texture():
    global w_last
    w_values = []
    for row in w_entries:
        for entry in row:
            val=entry.get()
            if val == '' or val=='-':
                entry.delete(0, tk.END)
                entry.insert(0,str(0))
                val=0
            w_values.append(float(val))
    while len(w_values) < w.size:
        w_values.append(0)
            
    if (not w_last is None) and np.linalg.norm(np.array(w_values)-w_last)==0:
        return
    w_last=w_values
    
    plot_vector(coef_to_vector(w_values, Vh))

def reset_plot_reconstructed_texture():
    global w_last
    w_last=None
    plot_reconstructed_texture()
    
def set_entries_to_zero():
    min_val = float(entry_min.get())
    max_val = float(entry_max.get())
    i=0
    for row in w_entries:
        for entry in row:
            if min_val <= i <= max_val:
                entry.delete(0, tk.END)
                entry.insert(0, str(0))
            i+=1

def update_selected_block():
    global base_block,w
    base_block=entry_block.get()
    try:
        read_block()
    except:
        messagebox.showerror("Block Not Found", base_block+"."+current_format+" was not found!")
        return

    i=0
    for row in w_entries:
        j=0
        for entry in row:
            val=round(w[i * num_cols + j],5)

            entry.delete(0,tk.END)
            entry.insert(0,str(val))
            j+=1
        i+=1
    
    plot_reconstructed_texture()


def blend_selected_block():
    global base_block,w,w2,w_last
    base_block=entry_block2.get()

    w3=w_last
    
    w2=w
    try:
        w2=read_block()

        if not w3 is None:
            w=np.array(w3)
        else:
            base_block=entry_block.get()

            w=read_block()
        
    except:
        messagebox.showerror("Block Not Found", base_block+"."+current_format+" was not found!")
        return
    
    p=min(max(0,float(blend_slider.get())/100.0),1)

    w=p * w2 + (1 - p) * w

    i=0
    for row in w_entries:
        j=0
        for entry in row:
            val=round(w[i * num_cols + j],2)

            entry.delete(0,tk.END)
            entry.insert(0,str(val))
            j+=1
        i+=1
    
    plot_reconstructed_texture()



entry_min = Entry(root, width=10)
entry_min.insert(0, str(0))
entry_min.pack(side=tk.LEFT, padx=5)
entry_max = Entry(root, width=10)
entry_max.insert(0, str(255))
entry_max.pack(side=tk.LEFT, padx=5)

set_to_zero_button = Button(root, text="Set Range to 0", command=set_entries_to_zero)
set_to_zero_button.pack(side=tk.LEFT, padx=5)

entry_block = Entry(root, width=20)
entry_block.insert(0, str(base_block))
entry_block.pack(side=tk.LEFT, padx=5)



load_preset_button = Button(root, text="Load Preset", command=update_selected_block)
load_preset_button.pack(side=tk.LEFT, padx=5)

entry_block2 = Entry(root, width=20)
entry_block2.insert(0, str(base_block2))
entry_block2.pack(side=tk.LEFT, padx=5)

blend_slider = Scale(root, from_=0, to=100, orient=tk.HORIZONTAL)
blend_slider.set(0)
blend_slider.pack(side=tk.LEFT, padx=5)

load_preset_button2 = Button(root, text="Blend Presets", command=blend_selected_block)
load_preset_button2.pack(side=tk.LEFT, padx=5)


brightness_block = Entry(root, width=20)
brightness_block.insert(0, str(0))
brightness_block.bind('<KeyRelease>', update_brightness)
brightness_block.pack(side=tk.LEFT, padx=5)




reconstruct_button = Button(root, text="Reconstruct Texture", command=reset_plot_reconstructed_texture)
reconstruct_button.pack()


root.mainloop()
