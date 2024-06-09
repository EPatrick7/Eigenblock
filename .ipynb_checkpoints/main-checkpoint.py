import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os
import glob
from ipywidgets import interact, FloatSlider


def output_plot(matrix):
    '''Renders a matrix as a matplot plot'''
    plt.imshow(matrix, cmap='gray', vmin=0, vmax=255)
    plt.axis('off')
    plt.show()

def plot_vector(vector):
    '''Unpacks a 256 Vector into a 16x16 matrix and plots it'''
    vector=np.transpose(vector)
    output_plot(vector.reshape(16,16))

def output_image(matrix):
    '''Outputs a matrix as a standard image file'''
    matrix_normalized = (matrix * 255).astype(np.uint8)
    image = Image.fromarray(matrix_normalized, mode='L')
    image.show()

def read_texture(file_path):
    '''Reads a single texture and returns it as a vector.'''
    image = Image.open(file_path)
    image_gray = image.convert('RGBA').convert('L')
    matrix = np.array(image_gray)
    return np.transpose(matrix.flatten())

          
            
def read_textures():
    '''Inputs all png files of 16x16 into a matrix in mean-deviation form'''
    textures = glob.glob(os.path.join("textures/", '*.png'))
    all_textures=[]

    for file_path in textures:
        image = Image.open(file_path)
        if image.size == (16, 16): #Throw out all not 16x16 images.
            image_gray = image.convert('RGBA').convert('L')
            matrix = np.array(image_gray)
            
            
            all_textures.append(matrix.flatten())
        
    all_textures=np.vstack(all_textures)

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
    return np.transpose(Vh)@w

#Get all textures and then compress each one into a row in a giant matrix
all_textures,row_means=read_textures()

#Perform singular value decomposition on the matrix
U,Svals,Vh=np.linalg.svd(all_textures, full_matrices=False)
S=np.diag(Svals)
#all_textures = U @ S @ Vh

dirt=read_texture("textures/diamond_block.png")

#w= Vh@(dirt)

#plot_vector(coef_to_vector(w,Vh))



def update_texture(coeff):
    w_new = coeff * Vh @ dirt
    reconstructed_texture = coef_to_vector(w_new, Vh)
    plot_vector(reconstructed_texture)

# Create an interactive slider to control the coefficient
interact(update_texture, coeff=FloatSlider(value=1.0, min=0.0, max=2.0, step=0.1))

