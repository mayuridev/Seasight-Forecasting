
import itertools
import os
#import simplekml
from seasight_forecasting import global_vars
from threading import Thread
from time import sleep, time

def sendKmlToLG(main, slave):
    command = "sshpass -p " + global_vars.lg_pass + " scp $HOME/" + global_vars.project_location \
        + "Seasight-Forecasting/django/" + global_vars.kml_destination_path + main \
        + " " + global_vars.lg_IP + ":/var/www/html/SF/" + global_vars.kml_destination_filename
    print(command)
    os.system(command)
    command = "sshpass -p " + global_vars.lg_pass + " scp $HOME/" + global_vars.project_location \
        + "Seasight-Forecasting/django/" + global_vars.kml_destination_path + slave + " " \
        + global_vars.lg_IP + ":/var/www/html/kml/slave_" + str(global_vars.screen_for_colorbar) + ".kml"
    print(command)
    os.system(command)
    command = "sshpass -p " + global_vars.lg_pass + " ssh " + global_vars.lg_IP \
        + " \"echo http://" + global_vars.lg_IP + ":81/SF/" + global_vars.kml_destination_filename + "?id=" + str(int(time()*100)) \
        + " > /var/www/html/kmls.txt\""
    print(command)
    os.system(command)

def sendKmlToLGCommon(filename):
    sendKmlToLG(filename, 'slave_{}.kml'.format(global_vars.screen_for_colorbar))

def sendKmlToLGHistoric(files):
    sendKmlToLG(files[0], files[1])

def threaded_function():
    files = os.listdir(global_vars.kml_destination_path)
    files = [i for i in files if i.startswith('historic')]
    main = []
    slave = []
    for elem in files:
        if elem.endswith('slave_{}.kml'.format(global_vars.screen_for_colorbar)):
            slave.append(elem)
        else:
            main.append(elem)
    for elem in itertools.cycle(list(zip(main, slave))):
        sendKmlToLGHistoric(elem)
        sleep(global_vars.sleep_in_thread)
        if global_vars.thread == False:
            print("thread finished...exiting")
            break

def startSendKMLThread():
    global_vars.thread = True
    thread = Thread(target = threaded_function)
    thread.name = 'SendKML'
    thread.start()

def stopSendKMLThread():
    global_vars.thread = False

def sendFlyToToLG(lat, lon, altitude, heading, tilt, pRange, duration):
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

def doRotation(playList, latitude, longitude, altitude, pRange):
    for angle in range(0, 360, 10):
        flyto = playList.newgxflyto(gxduration=1.0)
        #flyto.gxflytomode = simplekml.GxFlyToMode.smooth
        #flyto.altitudemode = simplekml.AltitudeMode.relativetoground

        #flyto.lookat.gxaltitudemode = simplekml.GxAltitudeMode.relativetoseafloor
        flyto.lookat.longitude = float(longitude)
        flyto.lookat.latitude = float(latitude)
        flyto.lookat.altitude = altitude
        flyto.lookat.heading = angle
        flyto.lookat.tilt = 77
        flyto.lookat.range = pRange

def cleanVerbose():
    fName = 'seasight_forecasting/static/scripts/verbose.txt'
    with open(fName, "w"):
        pass

def writeVerbose(text):
    fName = 'seasight_forecasting/static/scripts/verbose.txt'
    with open(fName, "a+") as f:
        f.seek(0)
        data = f.read()
        if len(data) > 0 :
            f.write("<br>")
        f.write(text)

def logprint(text):
    if global_vars.logs:
        print(text)

def cleanMainKML():
    command = "sshpass -p " + global_vars.lg_pass + " ssh " + global_vars.lg_IP \
        + " \"echo '' > /var/www/html/kmls.txt\""
    os.system(command)

def cleanSecundaryKML():
    string = "\"echo '<?xml version=\\\"1.0\\\" encoding=\\\"UTF-8\\\"?> \n" + \
        "<kml xmlns=\\\"http://www.opengis.net/kml/2.2\\\"" + \
        " xmlns:gx=\\\"http://www.google.com/kml/ext/2.2\\\"" + \
        " xmlns:kml=\\\"http://www.opengis.net/kml/2.2\\\" " + \
        " xmlns:atom=\\\"http://www.w3.org/2005/Atom\\\">\n" + \
        " <Document id=\\\"slave_" + str(global_vars.screen_for_colorbar) + "\\\"> \n" + \
        " </Document>\n" + \
        " </kml>\n' > /var/www/html/kml/slave_" + str(global_vars.screen_for_colorbar) + ".kml\""

    command = "sshpass -p " + global_vars.lg_pass + " ssh " + global_vars.lg_IP \
        + " " + string
    os.system(command)

def cleanLogoKML():
    string = "\"echo '<?xml version=\\\"1.0\\\" encoding=\\\"UTF-8\\\"?> \n" + \
        "<kml xmlns=\\\"http://www.opengis.net/kml/2.2\\\"" + \
        " xmlns:gx=\\\"http://www.google.com/kml/ext/2.2\\\"" + \
        " xmlns:kml=\\\"http://www.opengis.net/kml/2.2\\\" " + \
        " xmlns:atom=\\\"http://www.w3.org/2005/Atom\\\">\n" + \
        " <Document id=\\\"slave_" + str(global_vars.screen_for_logos) + "\\\"> \n" + \
        " </Document>\n" + \
        " </kml>\n' > /var/www/html/kml/slave_" + str(global_vars.screen_for_logos) + ".kml\""

    command = "sshpass -p " + global_vars.lg_pass + " ssh " + global_vars.lg_IP \
        + " " + string
    os.system(command)

def removeSFFolder():
    command = "sshpass -p " + global_vars.lg_pass + " ssh " + global_vars.lg_IP \
        + " rm -rf /var/www/html/SF"
    os.system(command)

def cleanKMLFiles():
    cleanMainKML()
    cleanSecundaryKML()

def cleanAllKMLFiles():
    cleanMainKML()
    cleanSecundaryKML()
    cleanLogoKML()
    removeSFFolder()