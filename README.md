# Learning from Las Vegas

## TODO Checklist

- [x] **get feature vectors for known architectural styles**
  - [ ] structure the datasets into one dataset
  - [x] get mean of feature embeddings for one image
  - [x] get feature embeddings for each group of images from a style
  - [x] get group mean vector of each group
  - [x] save those in a list

- [ ] **get feature vectors for the Las Vegas Strip**
  - [ ] structure the datasets into one dataset
  - [ ] get mean of feature embeddings per image
  - [ ] save the feature embeddings per image to a list / db

- [ ] **run similarity search with FAISS**
  - [ ] index both sets of vectors
  - [ ] run clustering algorithm on Las Vegas images?
  - [ ] run similarity measure
  - [ ] visualize the result
  - [ ] the result should best be clickable to see an image


## General Idea
This project tries to examine the visual vocabulary 
a neural networks learned with respect to urban architecture.

In the famous book "learning from las vegas" from 1972 by 
Robert Venturi, Denise Scott Brown, and Steven Izenour,
a visual vocabulary for Las Vegas is documented manually by domain experts.

## Data
**1) webscaping** Publicly available images of the city of Las Vegas will be
collected 
possible datasources:
- google street view api:

  * https://developers.google.com/maps/documentation/streetview?hl=de
    
- google street view packages for downloading images (all need Google API):

  * https://github.com/FluffyMaguro/Streetview-panorama-scraping
  * https://pypi.org/project/google-streetview/
  * https://pypi.org/project/sv-dlp/

**2) eventually undistort the data**:
  
  - [method survey](https://github.com/KangLiao929/Awesome-Deep-Camera-Calibration)
  - [Learning-based Camera Calibration](https://github.com/Easonyesheng/CCS)
  

**3) Architectural elements data -tagged images- of domain specialists**

* https://www.kaggle.com/datasets/dumitrux/architectural-styles-dataset **1**
* https://www.kaggle.com/datasets/gustavoachavez/architectural-styles-periods-dataset **1**
  
* https://old.datahub.io/dataset/architectural-heritage-elements-image-dataset  **not useful**
* [papers with code](https://paperswithcode.com/dataset/wikichurches) data: https://zenodo.org/records/5166987 or https://doi.org/10.5281/zenodo.5166987 -> [paper](https://arxiv.org/pdf/2108.06959.pdf) **1**
* https://www.kaggle.com/datasets/tompaulat/modernarchitecture **1**
* AIDA: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/IGNELZ  **not useful**
* https://archive.org/details/americanglossary00garn/page/n53/mode/1up?view=theater **not extracted**
* https://newenglandclassic.com/visual-architectural-element-glossary/ **not extracted**
* https://ia802804.us.archive.org/18/items/avisualdictionaryofarchitecture/A%20Visual%20Dictionary%20of%20Architecture.pdf **not extracted**
* https://www.kaggle.com/datasets/amaralibey/gsv-cities  **not useful**
* [collections of architectural images](https://guides.lib.umich.edu/c.php?g=282888&p=1885038)  **not useful**

## Approaches for Solving the Task:

* what is the task here: feature vector / embedding extraction -> distance matrix -> (hierarchical) clustering / knn -> maybe name new categories -> hierarchical classification on these
* 2nd option prototype: feature vector on each category of architecture -> feature vectors on images -> distance matrix -> group / cluster on these?

## Tools:

* **NumPy and SciPy**: For numerical computations in Python, NumPy can be used for efficient operations on arrays, and SciPy offers more advanced distance computation functions (e.g., scipy.spatial.distance.cdist) that can compute distances between two collections of vectors efficiently.
* **scikit-learn**: This library has efficient implementations for distance calculations and can handle large datasets. The pairwise_distances function can compute the distance matrix between two sets of vectors using various metrics (e.g., Euclidean, Manhattan).
* **FAISS (Facebook AI Similarity Search)**: Developed by Facebook AI Research, FAISS is designed for efficient similarity search and clustering of dense vectors. It is particularly effective for large-scale datasets and can compute similarity/distance matrices rapidly.
* **Annoy (Approximate Nearest Neighbors Oh Yeah)**: Annoy is a library optimized for memory usage and speed, making it suitable for computing distances between large sets of vectors. It's particularly good for nearest neighbor searches in high-dimensional spaces.
* **HNSW (Hierarchical Navigable Small World)**: HNSW is an algorithm implemented in libraries like nmslib that excels in high-dimensional nearest neighbor search, offering a good balance between accuracy and performance for large datasets.

  
## Transfer Learning / Feature Extraction - get embedding from Pre Trained model

A (state-of-the-art) pretrained neural network will be used 
for architecture classes datasets and on the Las Vegas Images
to get embeddings.

### Model choice:

**final choice**

DINOv2 

**further Research** 

* [hierarchical classification](https://towardsdatascience.com/https-medium-com-noa-weiss-the-hitchhikers-guide-to-hierarchical-classification-f8428ea1e076) --> article
* [Deep Learning Architect](https://arxiv.org/pdf/1812.01714.pdf) --> paper
* [HIERARCHICAL (MULTI-LABEL) ARCHITECTURAL IMAGE RECOGNITION AND CLASSIFICATION](https://caadria2021.org/wp-content/uploads/2021/03/caadria2021_039.pdf)  --> paper
* https://ceur-ws.org/Vol-2602/paper1.pdf

+ https://mediatum.ub.tum.de/doc/1693528/document.pdf

### Saving and Evaluating the Results
* Storing the Distance Matrix: Given the size of the resulting distance matrix, consider using efficient storage formats like HDF5 (with libraries such as h5py in Python) to save the matrix. HDF5 can handle large datasets and allows for partial reading/writing, which can be very useful for large matrices.
* Evaluating Results: Depending on your specific use case (e.g., clustering, nearest neighbor search), evaluate the results by looking at metrics relevant to your application. For instance, in clustering, you might look at silhouette scores, while for nearest neighbors, precision at k might be more relevant.

### Visualization:

- conditional image generation for the new visual vocabulary
- tsne or pcs visualization of latent space clusters of architectural concepts
- feature vector visualization: https://yosinski.com/deepvis
- XAI Method 


## Evaluation

- [FAISS](https://github.com/facebookresearch/faiss/wiki/Getting-started) [install](https://faiss.ai)
- [FAISS tutorial with database](https://thetisdev.hashnode.dev/building-an-image-search-engine-with-python-and-faiss)
- measure feature vector distances
- visualize with r-tsne
- visualize neurons for architectural features




