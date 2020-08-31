
from django.http import HttpResponseRedirect
from django.shortcuts import render
from seasight_forecasting import global_vars
from seasight_forecasting.utils import *
from seasight_forecasting.ConfigurationFile import *
from seasight_forecasting.CaseMethods import *
from seasight_forecasting.Demo import *

def index(request):
    LoadConfigFile()
    cleanVerbose()
    resetView()
    return render(request, 'index.html', {})

def run_historic(request):
    region = request.POST.get('region')
    dateFrom = request.POST.get('dateFrom')
    check = request.POST.get('check')
    dateTo = request.POST.get('dateTo')
    region = GetRegionFromFile(request.POST.get('region'))
    GenerateHistoricKML(region, dateFrom, check, dateTo)
    startSendKMLThread()
    flyToRegion(region)

def run_present(request):
    region = GetRegionFromFile(request.POST.get('region'))
    GenerateRealTimeKML(region)
    sendKmlToLGCommon(global_vars.kml_destination_filename)
    flyToRegion(region)

def run_future(request):
    region = GetRegionFromFile(request.POST.get('region'))
    GenerateFutureKML(region)
    sendKmlToLGCommon(global_vars.kml_destination_filename)
    flyToRegion(region)

def stop_thread():
    stopSendKMLThread()

def past(request):
    LoadConfigFile()
    min_date, max_date = GetDate()
    context = {'min_date': min_date, 'max_date': max_date}

    if request.method == 'POST':
        if request.POST.get("Submit") == "Submit":
            cleanVerbose()
            writeVerbose('Expect several minutes to complete...')
            run_historic(request)
        if request.POST.get("Stop") == "Stop":
            stop_thread()

    return render(request, 'past.html', context)

def present(request):
    LoadConfigFile()
    if request.method == 'POST':
        if request.POST.get("Submit") == "Submit":
            cleanVerbose()
            writeVerbose('Expect several minutes to complete...')
            run_present(request)
        if request.POST.get("Stop") == "Stop":
            stop_thread()

    return render(request, 'present.html', {})

def future(request):
    LoadConfigFile()
    if request.method == 'POST':
        if request.POST.get("Submit") == "Submit":
            cleanVerbose()
            writeVerbose('Expect several minutes to complete...')
            run_future(request)
        if request.POST.get("Stop") == "Stop":
            stop_thread()

    return render(request, 'future.html', {})

def demo(request):
    LoadConfigFile()
    if request.method == 'POST':
        if request.POST.get("Start") == "Start":
            cleanVerbose()
            GenerateDemo()
        if request.POST.get("Stop") == "Stop":
            StopDemo()
    return render(request, 'demo.html', {})

def clean_KML(request):
    cleanKMLFiles()
    return HttpResponseRedirect("/")

def clean_ALL(request):
    cleanAllKMLFiles()
    return HttpResponseRedirect("/")