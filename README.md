# Python 'Eigenfaces' Implementation
My goal for this project was to play around with Eigenfaces and see what they can do when extended to non-human images in addition to the standard human datasets.

The program reads in a set of images of a predetermined (square) size and converts each image into a vector. It then stiches those vectors together into one gargantuan matrix and performs Singular Value Decomposition on it. Eigenfaces is a surprisingly versatile technique that utilizes the SVD of this dataset matrix.

Dataset = U * S * V^T
Where S is a diagonal matrix of singular values for the matrix.

By converting any image (of the same size as our dataset) into a vector and multiplying it against V^T we get out a vector of values that can represent something close to a unique identifier for our image. We can use the output vector to reconstruct the original image, or compare it against "similar" in value nearby vectors which would represent "similar" images in the vector space should the need arise. Eigenfaces are known to be a surprisingly effective facial recognition technique.

![EigenBlock_UI1](https://github.com/EPatrick7/Eigenblock/assets/88292909/a67d2b4b-0cc0-4884-8449-3501b50c50ee)


# Outputs
These outputs were images that were converted into greyscale 102 dimensional vector representations of themselves and then retransformed back into images using our database matrix of images that do not contain these test pictures at all.

<img width="400" alt="EigenBlockOutput_1" src="https://github.com/EPatrick7/Eigenblock/assets/88292909/391ea0c2-aa56-44c1-ad58-c32ea5499f3e">
<img width="400" alt="EigenBlock_Output_2" src="https://github.com/EPatrick7/Eigenblock/assets/88292909/6bc9586b-bcbf-486e-8758-278e81e5e39f">


# Real Images
One of the sliders I had in the program limited how many images of the larger human face dataset were allowed to be incorporated into the database matrix. The reliable reproduction of non-database images from vectorization seemed to only be of reasonable quality when the matrix database was allowed a decent amount of input images.

![TestBlock](https://github.com/EPatrick7/Eigenblock/assets/88292909/7bbfc91c-a4be-4bf8-ad0a-ae9f1e7713be)
![TestPhoto](https://github.com/EPatrick7/Eigenblock/assets/88292909/c1671800-1081-461c-8544-c6dd26f4466c)

# Note: 
Currently this implementation only supports greyscale images and images of known square sizes.

Human Datasets From:
https://figshare.com/articles/dataset/Face_Research_Lab_London_Set/5047666?file=8541961
https://vis-www.cs.umass.edu/lfw/
