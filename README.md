# Beat the Heat
is a computer science senior design project that uses machine learning to predict fire incidents in California based on sattelite data and past fire records. 

# The purpose
of this project is to apply new technologies to real world problems that are devistating people's lives and destroying forrests in California. Beat the Heat predicts whether or not there will be a fire in a region given the conditions on that day. The project does this both for the entire state of California as well as at the county level. The features/conditions from remote sensing data used for the models are land surface temperature (LST), thermal anomaly (TA, aka fire detector), and normalized difference vegetation index (NDVI, aka greenness). Another remote sensing feature, burned area, was also used to only examine data from areas that had been burned within a month of a specific day. The highest accuracy score at the state level was 93% for support vector machine, and 98% at the county level.

# What's included
All of the code related to preprocessing the datasets and running/tweaking the models can be found here. The only missing components are the remote sensing sattelite images, which can be accessed for free and downloaded after making an account from the Land Processes Distributed Active Archive Center (LP DAAC) website (https://lpdaac.usgs.gov). Please contact us if there are questions on how to access this information or view our conference paper.

# Data preprocessing
Two datasets were created to analyze California: one that treats California as one region and the other that breaks California down into 58 counties and analyzed at the county level for the purpose of averaging conditions in a region and flagging the condition with fire or no fire for model training (via the included fire incident record via CA Fire, https://www.fire.ca.gov). Counties were selected over finer spatial resolution areas such as per 500m/1km grid cells because in the final dataset because the data is being classified into fire or no fire categories via CA fire incident record of which the smallest spatial resolution was at the county level (see combining_datasets/mapdataall.csv for more details).

## Dependancies/Running instructions
MacOS users may not be able to download dependant software such as GDAL or Rasterio as there are known issues. Windows 10 and Anaconda package manager was used by all members in the project. There are a number of dependancies in this project related to interpretering and analyzing sattelite image files. Anaconda and Pip may be used to install the libaries, however if that does not work as was the case for many of us, we recommend downloading the windows binary version of each library (https://www.lfd.uci.edu/~gohlke/pythonlibs/) and install using Anaconda Powershell as described in this helpful video (https://www.youtube.com/watch?v=LNPETGKAe0c).

 The project is dependant on the following software: 
* Python 3.8.3
* GDAL
* Rasterio
* Fiona



#### The senior design project was for California State University Northridge (CSUN). Group members include: Kaylee Pham, David Shin, Saulo Rubio, Tyler Poplawski, Sergio Ramirez, and David Macoto Ward.

Analysis was done in Python. Thank you to the authors of "Predictive modeling of wildfires: a new dataset" for detailing many of the steps followed  https://www.frames.gov/catalog/57447
