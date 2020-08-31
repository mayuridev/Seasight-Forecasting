
import configparser
from seasight_forecasting import global_vars

def LoadConfigFile():
    config = configparser.ConfigParser()
    configFilePath = r'app.conf'
    config.read(configFilePath)

    global_vars.historic_file_path = config['FILES']['historic_data_path'] + config['FILES']['historic_data_file']
    global_vars.prediction_model_path = config['FILES']['prediction_model_path'] + config['FILES']['prediction_model_file']
    global_vars.prediction_model_weights = config['FILES']['prediction_model_path'] + config['FILES']['prediction_model_weights']
    global_vars.north_atlantic_region_path = config['FILES']['regions_path'] + config['FILES']['north_atlantic_region_file']
    global_vars.south_atlantic_region_path = config['FILES']['regions_path'] + config['FILES']['south_atlantic_region_file']
    global_vars.indian_region_path = config['FILES']['regions_path'] + config['FILES']['indian_region_file']
    global_vars.west_pacific_region_path = config['FILES']['regions_path'] + config['FILES']['west_pacific_region_file']
    global_vars.north_east_pacific_region_path = config['FILES']['regions_path'] + config['FILES']['north_east_pacific_region_file']
    global_vars.south_east_pacific_region_path = config['FILES']['regions_path'] + config['FILES']['south_east_pacific_region_file']
    global_vars.kml_destination_path = config['FILES']['kml_destination_path']
    global_vars.kml_destination_filename = config['FILES']['kml_destination_file']
    global_vars.image_destination_path = config['FILES']['image_destination_path']
    global_vars.demo_files_path = config['FILES']['demo_files_path']

    global_vars.number_of_clusters = int(config['KML']['number_of_clusters'])
    global_vars.cmap = config['KML']['cmap']
    global_vars.sleep_in_thread = int(config['KML']['sleep_in_thread'])
    global_vars.altitude = int(config['KML']['altitude'])
    global_vars.pRange = int(config['KML']['range'])

    global_vars.server_IP = config['INSTALLATION']['server_IP']
    global_vars.lg_IP = config['INSTALLATION']['lg_IP']
    global_vars.lg_pass = config['INSTALLATION']['lg_pass']
    global_vars.screen_for_logos = int(config['INSTALLATION']['screen_for_logos'])
    global_vars.screen_for_colorbar = int(config['INSTALLATION']['screen_for_colorbar'])
    global_vars.project_location = config['INSTALLATION']['project_location']
    global_vars.logs = config['INSTALLATION']['logs']
    global_vars.show_verbose = config['INSTALLATION']['show_verbose']

    print('Global variables loaded!')
