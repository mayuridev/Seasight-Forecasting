
import os
from seasight_forecasting import global_vars
from seasight_forecasting.Clustering import *
from seasight_forecasting.GenerateKML import *
from seasight_forecasting.ManageData import *
from seasight_forecasting.ManageModel import *
from seasight_forecasting.utils import *

def GetDate():
    data = LoadData(global_vars.historic_file_path)
    data.time = pd.to_datetime(data.time, errors='coerce', format='%Y-%m-%d %H:%M:%S')
    min_date = str(data.time.min().date())
    max_date = str(data.time.max().date())
    return min_date, max_date

def PrepareData(data):
    data.time = pd.to_datetime(data.time, errors='coerce', format='%Y-%m-%d %H:%M:%S')
    data.lon = pd.to_numeric(data.lon, errors='coerce').fillna(0).astype(float)
    data.lat = pd.to_numeric(data.lat, errors='coerce').fillna(0).astype(float)
    data.sst = round(pd.to_numeric(data.sst, errors='coerce').fillna(0).astype(float), 1)
    return data

def RemoveOldHistoricFiles():
    dir_name = global_vars.kml_destination_path
    files = os.listdir(dir_name)

    for item in files:
        if item.startswith("historic"):
            os.remove(os.path.join(dir_name, item))

def CreateSingleFrameKML(data):
    print('Number of clusters: {}'.format(global_vars.number_of_clusters))
    message = 'Start Clustering...'
    print(message)
    writeVerbose(message)
    data = GetClusters(global_vars.number_of_clusters, data)
    regions = GetRegions(global_vars.number_of_clusters, data, InitCmap(data.sst.min(), data.sst.max()))
    message = 'Clustering DONE!'
    print(message)
    writeVerbose(message)
    CreateKML(regions, False)
    return 'Created KML files in {}'.format(global_vars.kml_destination_path)

def GenerateHistoricKML(region, dateFrom, check, dateTo):
    data = LoadData(global_vars.historic_file_path)
    writeVerbose('Data loading DONE')
    data = PrepareData(data)
    logprint(data)
    print('ORIGINAL DATA')

    message = 'Start date and region filtering...'
    print(message)
    writeVerbose(message)
    data = GetDataInDateRange(data, dateFrom, check, dateTo)
    logprint(data)
    print('DATA AFTER DATE FILTER')

    data = GetDataFromRegion(data, region)
    logprint(data)
    print('DATA AFTER REGION FILTER')
    writeVerbose('Data filtering DONE')

    try:
        print('Number of clusters: {}'.format(global_vars.number_of_clusters))
        message = 'Start Clustering...'
        print(message)
        writeVerbose(message)
        RemoveOldHistoricFiles()
        for group in data.groupby(['time']):
            data = group[1]
            data = data.drop(['time'], axis=1)
            ngroup = GetClusters(global_vars.number_of_clusters, data)
            regions = GetRegions(global_vars.number_of_clusters, ngroup, InitCmap(data.sst.min(), data.sst.max()))
            CreateKML(regions, group[0].date())
        message = 'Created KML files in {}'.format(global_vars.kml_destination_path)
    except Exception as e:
        message = "ERROR: {}".format(e)
    print(message)
    writeVerbose(message)

def GenerateRealTimeKML(region):
    data = GetDataFromAPI()
    data = PrepareData(data)
    data = data.drop(['time'], axis=1)
    logprint(data)
    print('ORIGINAL DATA')

    message = 'Start region filtering...'
    print(message)
    writeVerbose(message)
    data = GetDataFromRegion(data, region)
    logprint(data)
    print('DATA AFTER REGION FILTERING')
    writeVerbose('Data filtering DONE')

    try:
        message = CreateSingleFrameKML(data)
    except Exception as e:
        message = "ERROR: {}".format(e)
    print(message)
    writeVerbose(message)

def GenerateFutureKML(region):
    data = LoadData(global_vars.historic_file_path)
    data = data[data.time == data.time.tail(1)[data.time.tail(1).index._start]]
    data = PrepareData(data)
    data = data.drop(['time'], axis=1)
    logprint(data)
    print('ORIGINAL DATA')

    message = 'Start region filtering...'
    print(message)
    writeVerbose(message)
    data = GetDataFromRegion(data, region)
    logprint(data)
    print('DATA AFTER REGION FILTERING')
    writeVerbose('Data filtering DONE')

    message = 'Start Prediction...'
    print(message)
    writeVerbose(message)
    data = PredictedData(data)
    logprint(data)
    print('PREDICTED DATA')
    message = 'Prediction DONE!'
    print(message)
    writeVerbose(message)

    try:
        message = CreateSingleFrameKML(data)
    except Exception as e:
        message = "ERROR: {}".format(e)
    print(message)
    writeVerbose(message)