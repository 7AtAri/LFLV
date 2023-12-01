# Learning from Las Vegas

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
    
- google street view:

  * https://github.com/FluffyMaguro/Streetview-panorama-scraping
  * https://pypi.org/project/google-streetview/
  * https://pypi.org/project/sv-dlp/
  
- google image search
- ...
  
**2) undistort the data**:
  
  - [method survey](https://github.com/KangLiao929/Awesome-Deep-Camera-Calibration)
  - [Learning-based Camera Calibration](https://github.com/Easonyesheng/CCS)
  

**3) tagging the data** / parts of the data (maybe only for testing?) 

*  Optical Character Recognition: https://github.com/aqntks/Easy-Yolo-OCR
*  Object Recognition Model (YOLO)
*  adding tag to image of object in closest proximity to the text

**4) Architectural elements data -tagged images- of domain specialist**

* https://archive.org/details/americanglossary00garn/page/n53/mode/1up?view=theater
* https://newenglandclassic.com/visual-architectural-element-glossary/


## Transfer Learning

A (state-of-the-art) pretrained neural network will be fine-tuned on the Las Vegas Images.

-> classification ?
-> conditional image generation?

## Evaluation

- measure feature vector distances
- visualize with r-tsne
- visualize neurons for architectural features
- 



