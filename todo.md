# TODO Checklist

- [ ] **get feature vectors for known architectural styles**
  - [ ] structure the datasets into one dataset
  - [ ] get mean of feature embeddings for one image
  - [ ] get feature embeddings for each group of images from a style
  - [ ] get group mean vector of each group
  - [ ] save those in a list

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
