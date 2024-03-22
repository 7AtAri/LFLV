# Learning from Las Vegas

## TODO Checklist

- [x] **get feature vectors for known architectural styles**
  - [x] get mean of feature embeddings for one image
  - [x] get feature embeddings for each group of images from a style
  - [x] get group mean vector of each group
  - [x] save those in a json 

- [x] **get feature vectors for the Las Vegas Strip**
  - [x] structure the datasets into one dataset
  - [x] get mean of feature embeddings per image
  - [x] save/pickle the feature embeddings per image (npz matrix)

- [x] **run similarity search / calculate a distance matrix**
  - [x] run clustering algorithm on Las Vegas images
  - [x] calc distance matrix
  - [x] visualize the result


## General Idea
In the famous book "learning from las vegas" from 1972 by 
Robert Venturi, Denise Scott Brown, and Steven Izenour,
a visual vocabulary for Las Vegas is clustered manually by domain experts.
It was a foundational text for postmodern architecture.

This project tries to examine the visual vocabulary 
a neural network can learn with respect to urban architecture.
Therefore google street view images of the Las Vegas Strip are 
embedded with DINOv2 and compared with embeddings from a dataset
of architectural styles.





