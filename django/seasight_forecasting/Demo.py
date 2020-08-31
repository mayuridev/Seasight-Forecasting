
import os
from seasight_forecasting import global_vars
from seasight_forecasting.utils import *
from time import sleep, time

def sendKmlToLGDemo(main, slave):
    command = "sshpass -p " + global_vars.lg_pass + " scp $HOME/" + global_vars.project_location \
        + "Seasight-Forecasting/django/" + main + "SST_regions.kml " + global_vars.lg_IP + ":/var/www/html/SF/" + global_vars.kml_destination_filename
    print(command)
    os.system(command)

    command = "sshpass -p " + global_vars.lg_pass + " scp $HOME/" + global_vars.project_location \
        + "Seasight-Forecasting/django/" + main + "orbit.kml " + global_vars.lg_IP + ":/var/www/html/SF/orbit.kml"
    print(command)
    os.system(command)

    command = "sshpass -p {} scp $HOME/{}Seasight-Forecasting/django/seasight_forecasting/static/kml/DEMO/colorbar.png {}:/var/www/html/SF/colorbar.png".format(global_vars.lg_pass, global_vars.project_location, global_vars.lg_IP)
    print(command)
    os.system(command)
    command = "sshpass -p " + global_vars.lg_pass + " ssh " + global_vars.lg_IP \
        + " \"echo "  \
        + " > /var/www/html/kml/slave_" + str(global_vars.screen_for_colorbar) + ".kml\""
    print(command)
    os.system(command)
    command = "sshpass -p " + global_vars.lg_pass + " scp $HOME/" + global_vars.project_location \
        + "Seasight-Forecasting/django/" + slave + " " \
        + global_vars.lg_IP + ":/var/www/html/kml/slave_" + str(global_vars.screen_for_colorbar) + ".kml"
    print(command)
    os.system(command)

    command = "sshpass -p " + global_vars.lg_pass + " ssh " + global_vars.lg_IP \
        + " \"echo http://" + global_vars.lg_IP + ":81/SF/" + global_vars.kml_destination_filename + "?id=" + str(int(time()*100)) + " > /var/www/html/kmls.txt\""
    print(command)
    os.system(command)
    command = "sshpass -p " + global_vars.lg_pass + " ssh " + global_vars.lg_IP \
        + " \"echo http://" + global_vars.lg_IP + ":81/SF/orbit.kml?id=" + str(int(time()*100)) + " >> /var/www/html/kmls.txt\""
    print(command)
    os.system(command)

def sendFlyToToLGDemo(lat, lon, altitude, heading, tilt, pRange, duration):
    flyTo = "flytoview=<LookAt>" \
            + "<longitude>" + str(lon) + "</longitude>" \
            + "<latitude>" + str(lat) + "</latitude>" \
            + "<altitude>" + str(altitude) + "</altitude>" \
            + "<heading>" + str(heading) + "</heading>" \
            + "<tilt>" + str(tilt) + "</tilt>" \
            + "<range>" + str(pRange) + "</range>" \
            + "<altitudeMode>relativeToGround</altitudeMode>" \
            + "<gx:altitudeMode>relativeToGround</gx:altitudeMode>" \
            + "<gx:duration>" + str(duration) + "</gx:duration>" \
            + "</LookAt>"

    command = "echo '" + flyTo + "' | sshpass -p " + global_vars.lg_pass + " ssh " + global_vars.lg_IP + " 'cat - > /tmp/query.txt'"
    print(command)
    os.system(command)

def createRotationDemo(lat, lon, alt, tilt, fovy, range1):
    xml = '<?xml version="1.0" encoding="UTF-8"?>'
    xml += '\n'+'<kml xmlns="http://www.opengis.net/kml/2.2"'
    xml += '\n'+'xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">'
    xml += '\n'+'<gx:Tour>'
    xml += '\n\t'+'<name>Orbit</name>'
    xml += '\n\t'+'<gx:Playlist>'
    for i in range(0,360,10):
        xml += '\n\t\t'+'<gx:FlyTo>'
        xml += '\n\t\t\t'+'<gx:duration>1.2</gx:duration>'
        xml += '\n\t\t\t'+'<gx:flyToMode>smooth</gx:flyToMode>'
        xml += '\n\t\t\t'+'<LookAt>'
        xml += '\n\t\t\t\t'+'<longitude>'+str(lon)+'</longitude>'
        xml += '\n\t\t\t\t'+'<latitude>'+str(lat)+'</latitude>'
        xml += '\n\t\t\t\t'+'<altitude>'+str(alt)+'</altitude>'
        xml += '\n\t\t\t\t'+'<heading>'+str(i)+'</heading>'
        xml += '\n\t\t\t\t'+'<tilt>'+str(tilt)+'</tilt>'
        xml += '\n\t\t\t\t'+'<gx:fovy>'+str(fovy)+'</gx:fovy>'
        xml += '\n\t\t\t\t'+'<range>'+str(range1)+'</range>'
        xml += '\n\t\t\t\t'+'<gx:altitudeMode>absolute</gx:altitudeMode>'
        xml += '\n\t\t\t'+'</LookAt>'
        xml += '\n\t\t'+'</gx:FlyTo>'

    xml += '\n\t'+'</gx:Playlist>'
    xml += '\n'+'</gx:Tour>'
    xml += '\n'+'</kml>'
    return xml

def generateOrbitFileDemo(content, path):
    with open(path, 'w') as file1:
        file1.write(content)

def LoadKML(path):
    sendKmlToLGDemo(path, path + 'slave.kml')

def FlyTo(center_lat, center_lon):
    sendFlyToToLGDemo(center_lat, center_lon, global_vars.altitude, 0, 0, global_vars.pRange, 3)

def Rotate(center_lat, center_lon, path):
    content = createRotationDemo(center_lat, center_lon, global_vars.altitude, 5, 35, global_vars.pRange)
    path = path + 'orbit.kml'
    generateOrbitFileDemo(content, path)

def startRotation():
    command = "sshpass -p " + global_vars.lg_pass + " ssh " + global_vars.lg_IP + " \'echo \'playtour=Orbit\' > /tmp/query.txt\'"
    os.system(command)

def stopRotation():
    command = "sshpass -p " + global_vars.lg_pass + " ssh " + global_vars.lg_IP + " \'echo \'exittour=true\' > /tmp/query.txt\'"
    os.system(command)

def SouthAtlantic():
    path = global_vars.demo_files_path + 'South_Atlantic/'
    coords = [-44.033173405198575, -18.55412927249652]
    Rotate(coords[0], coords[1], path)
    writeVerbose('Start region filtering...')
    sleep(1)
    writeVerbose('Data filtering DONE')
    writeVerbose('Start Prediction...')
    sleep(1)
    writeVerbose('Prediction DONE!')
    writeVerbose('Start Clustering...')
    sleep(1)
    writeVerbose('Clustering DONE!')
    sleep(1)
    writeVerbose('Created KML files')
    LoadKML(path)
    writeVerbose('Flying to the position...')
    FlyTo(coords[0], coords[1])
    sleep(3)
    writeVerbose('Rotating...')
    startRotation()
    sleep(30)

def Indian():
    path = global_vars.demo_files_path + 'Indian/'
    coords = [-20.55819005127296, 71.46322969298124]
    Rotate(coords[0], coords[1], path)
    writeVerbose('Start region filtering...')
    sleep(1)
    writeVerbose('Data filtering DONE')
    writeVerbose('Start Prediction...')
    sleep(1)
    writeVerbose('Prediction DONE!')
    writeVerbose('Start Clustering...')
    sleep(1)
    writeVerbose('Clustering DONE!')
    sleep(1)
    writeVerbose('Created KML files')
    LoadKML(path)
    writeVerbose('Flying to the position...')
    FlyTo(coords[0], coords[1])
    sleep(3)
    writeVerbose('Rotating...')
    startRotation()
    sleep(30)

def WestPacific():
    path = global_vars.demo_files_path + 'West_Pacific/'
    coords = [-3.6055350414132112, 148.72609606570853]
    Rotate(coords[0], coords[1], path)
    writeVerbose('Start region filtering...')
    sleep(1)
    writeVerbose('Data filtering DONE')
    writeVerbose('Start Prediction...')
    sleep(1)
    writeVerbose('Prediction DONE!')
    writeVerbose('Start Clustering...')
    sleep(1)
    writeVerbose('Clustering DONE!')
    sleep(1)
    writeVerbose('Created KML files')
    LoadKML(path)
    writeVerbose('Flying to the position...')
    FlyTo(coords[0], coords[1])
    sleep(3)
    writeVerbose('Rotating...')
    startRotation()
    sleep(30)

def EastPacific():
    path = global_vars.demo_files_path + 'East_Pacific/'
    coords = [-14.22202896516345, -129.23682168130628]
    Rotate(coords[0], coords[1], path)
    writeVerbose('Start region filtering...')
    sleep(1)
    writeVerbose('Data filtering DONE')
    writeVerbose('Start Prediction...')
    sleep(1)
    writeVerbose('Prediction DONE!')
    writeVerbose('Start Clustering...')
    sleep(1)
    writeVerbose('Clustering DONE!')
    sleep(1)
    writeVerbose('Created KML files')
    LoadKML(path)
    writeVerbose('Flying to the position...')
    FlyTo(coords[0], coords[1])
    sleep(3)
    writeVerbose('Rotating...')
    startRotation()
    sleep(30)

def NorthAtlantic():
    path = global_vars.demo_files_path + 'North_Atlantic/'
    coords = [43.090963600753945, -25.84386342158867]
    Rotate(coords[0], coords[1], path)
    writeVerbose('Start region filtering...')
    sleep(1)
    writeVerbose('Data filtering DONE')
    writeVerbose('Start Prediction...')
    sleep(1)
    writeVerbose('Prediction DONE!')
    writeVerbose('Start Clustering...')
    sleep(1)
    writeVerbose('Clustering DONE!')
    sleep(1)
    writeVerbose('Created KML files')
    LoadKML(path)
    writeVerbose('Flying to the position...')
    FlyTo(coords[0], coords[1])
    sleep(3)
    writeVerbose('Rotating...')
    startRotation()
    sleep(30)

def demo_threaded_function():
    while 1:
        SouthAtlantic()
        if global_vars.thread == False: break
        Indian()
        if global_vars.thread == False: break
        WestPacific()
        if global_vars.thread == False: break
        EastPacific()
        if global_vars.thread == False: break
        NorthAtlantic()
        if global_vars.thread == False: break

def startDemoThread():
    global_vars.thread = True
    thread = Thread(target = demo_threaded_function)
    thread.name = 'Demo'
    thread.start()

def cleanVerboseDemo():
    fName = 'seasight_forecasting/static/scripts/verbose.txt'
    with open(fName, "w"):
        pass

def GenerateDemo():
    cleanVerboseDemo()
    startDemoThread()

def StopDemo():
    global_vars.thread = False
    stopRotation()