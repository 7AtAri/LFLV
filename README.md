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
  
- google image search:
  * https://pypi.org/project/GoogleImageScraper/
    
- mapillary image download via API:
  * token: MLY|6919611378086321|feb37f9b9d4e6dc4ca37b7a6a862f43c
  * client ID: 6919611378086321 
  * https://github.com/pyramid3d/python-tools/blob/master/src/mapillary_download.py  -> date and driver
  * https://gist.github.com/cbeddow/79d68aa6ed0f028d8dbfdad2a4142cf5  -> bounding box
  * https://www.mapillary.com/developer/api-documentation?locale=de_DE#image
    
**2) eventually undistort the data**:
  
  - [method survey](https://github.com/KangLiao929/Awesome-Deep-Camera-Calibration)
  - [Learning-based Camera Calibration](https://github.com/Easonyesheng/CCS)
  

**3) eventually tagging the data** / parts of the data (maybe only for testing?) 

*  Optical Character Recognition: https://github.com/aqntks/Easy-Yolo-OCR
*  Object Recognition Model (YOLO)
*  adding tag to image of object in closest proximity to the text

**4) Architectural elements data -tagged images- of domain specialists**

* https://www.kaggle.com/datasets/dumitrux/architectural-styles-dataset
* [papers with code](https://paperswithcode.com/dataset/wikichurches) data: https://zenodo.org/records/5166987 -> [paper](https://arxiv.org/pdf/2108.06959.pdf)
* https://archive.org/details/americanglossary00garn/page/n53/mode/1up?view=theater
* https://newenglandclassic.com/visual-architectural-element-glossary/
* https://ia802804.us.archive.org/18/items/avisualdictionaryofarchitecture/A%20Visual%20Dictionary%20of%20Architecture.pdf

* https://www.kaggle.com/datasets/amaralibey/gsv-cities


## Transfer Learning

A (state-of-the-art) pretrained neural network will be fine-tuned on the Las Vegas Images.

-> classification ?

-> feature vector visualization: https://yosinski.com/deepvis

-> conditional image generation?

## Evaluation

- measure feature vector distances
- visualize with r-tsne
- visualize neurons for architectural features
- metric for creativity? https://github.com/facebookresearch/DoodlerGAN



