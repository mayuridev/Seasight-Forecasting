# Seasight-Forecasting

## __Google Summer Of Code 2020__
<p align="center">
    <img width="600" src="https://jderobot.github.io/assets/images/activities/gsoc-2020.jpg">
</p>

__Welcome to Seasight Forecasting project__

This project is developed in a context of a scolarship in the program Google Summer Of Code 2020 and is a web application based on Django that pretends to display on the Liquid Galaxy sea surface temperatures based on 3 use cases: display historic temperatures, display real time temperatures and display predicted temperatures.

<p align="center">
 <img width="200" src="django/seasight_forecasting/static/logos/SF-logo.png">
</p>

## Source files

The application runs in a Django environment, so the files that are part of its structure will not be listed.

Below are the files that contain the core of the application and the functions needed for it to work properly

```bash
────Seasight-Forecasting
    │   .cdsapirc
    │
    ├───data
    │   │   historic.csv
    │   │
    │   └───regions
    │           east_pacific.geojson
    │           indian.geojson
    │           north_atlantic.geojson
    │           north_east_pacific.geojson
    │           south_atlantic.geojson
    │           south_east_pacific.geojson
    │           west_pacific.geojson
    │
    └───django
        │   app.conf
        │   requirements.txt
        │   setMasterFiles.py
        │   startDjango.py
        │
        └───seasight_forecasting
                CaseMethods.py
                Clustering.py
                ConfigurationFile.py
                Demo.py
                GenerateKML.py
                global_vars.py
                ManageData.py
                ManageModel.py
                tests.py
                utils.py
```
- **.cdsapirc**: API credentials file. Contains the credentials that enable communication between the application and the API.
- **data/historic.csv**: File that contains historical data that is used by the "Historic" section of the application.
- **data/regions/*.geojson**: List of geojson files that contains the polygon coordinates of the different ocean regions.
- **django/app.conf**: Configuration file with customizable parameters. The parameters of this file are described below.
- **django/requirements.txt**: File with the required packages for the application to work properly.
- **django/seasight_forecasting/CaseMethods.py**: This file contains the main methods for the different cases (Historic, Real-time, Future).
- **django/seasight_forecasting/Clustering.py**: This file contains the methods to group the data and obtain the coordinates of the polygons in these groups. In addition to the methods to obtain the colormap and the colors of the regions.
- **django/seasight_forecasting/ConfigurationFile.py**: This file contains the initialization of the configuration file by dumping its content into global variables.
- **django/seasight_forecasting/Demo.py**: This file contains the methods to run the Demo section.
- **django/seasight_forecasting/GenerateKML.py**: This file contains the methods to create the KML file.
- **django/seasight_forecasting/global_vars.py**: This file contains a list of global variable that are filled with information from configuration file.
- **django/seasight_forecasting/ManageData.py**: This file contains the methods related to data management: filtering, data loading, data from API downloading, ...
- **django/seasight_forecasting/ManageModel.py**: This file contains the methods related to Deep Learning model management: model loading, data prediction, ...
- **django/seasight_forecasting/tests.py**: This file contains the list of the application tests.
- **django/seasight_forecasting/utils.py**: This file contains the common methods to run threads, create and send files, send FlyTo and Orbits, ...

### Configuration File
```bash
[FILES]
historic_data_path = ../data/
historic_data_file = historic.csv
prediction_model_path = ../model/
prediction_model_file = lr_model.pkl
prediction_model_weights = model1.h5
regions_path = ../data/regions/
north_atlantic_region_file = north_atlantic.geojson
south_atlantic_region_file = south_atlantic.geojson
indian_region_file = indian.geojson
west_pacific_region_file = west_pacific.geojson
north_east_pacific_region_file = north_east_pacific.geojson
south_east_pacific_region_file = south_east_pacific.geojson
kml_destination_path = seasight_forecasting/static/kml/
kml_destination_file = SST_regions.kml
image_destination_path = seasight_forecasting/static/img/
demo_files_path = seasight_forecasting/static/kml/DEMO/

[KML]
number_of_clusters = 200
cmap = PRGn
sleep_in_thread = 2
altitude = 15000
range = 6000000

[INSTALLATION]
server_IP = 192.168.10.121
lg_IP = lg@10.160.67.94
lg_pass = lq
screen_for_logos = 4
screen_for_colorbar = 3
project_location = Projects/
logs = False
show_verbose = True
```

- **[FILES] section**: This section includes all paths and file names of non-application data.
- **[KML] section**: This section includes the necessary parameters for the KML creation, such as the number of clusters to display, the colormap for the regions color, the time between the historic KMLs and parameters related to the altitude and the range of the FlyTo.
- **[INSTALLATION] section**: This section includes IPs of the server and the Liquid Galaxy, the screens the user wants to display the logos and colorbar and the project location folder.

## Installing / Getting started
[Install Guide](../master/docs/INSTALL.md)

### Built With
Python3, Django

## License
[Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/)