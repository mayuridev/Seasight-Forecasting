# -*- coding: utf-8 -*-

# Import libraries
import itertools
from lxml import etree
from pykml.factory import KML_ElementMaker as KML
from seasight_forecasting import global_vars

def GetCoords(region):
    string = ''
    for p in region:
        string += '{},{},40000\n'.format(p[0], p[1])
    return string

def CreateDateAndColorbarKML(date):
    kml = KML.kml(
        KML.Document(
            KML.Folder(
                KML.ScreenOverlay(
                    KML.name('Colorbar'),
                    KML.Icon(KML.href('http://lg1:81/SF/colorbar.png')),
                    KML.overlayXY(x="0", y="1", xunits="fraction", yunits="fraction"),
                    KML.screenXY(x="0.75", y="0.8", xunits="fraction", yunits="fraction"),
                    KML.rotationXY(x="0", y="0", xunits="fraction", yunits="fraction"),
                    KML.size(x="0.25", y="0.6", xunits="fraction", yunits="fraction")
                )
            )
        )
    )

    filename = 'slave_{}.kml'.format(global_vars.screen_for_colorbar)

    if date:
        filename = 'historic_' + str(date) + "_" + filename
        print(filename)

    if date:
        kml.Document.Folder.append(
                KML.ScreenOverlay(
                    KML.name('Date'),
                    KML.Icon(KML.href('http://chart.apis.google.com/chart?chst=d_text_outline&chld=FFFFFF|20|h|000000|_|{}'.format(date))),
                    KML.overlayXY(x="0", y="1", xunits="fraction", yunits="fraction"),
                    KML.screenXY(x="0.02", y="0.95", xunits="fraction", yunits="fraction"),
                    KML.rotationXY(x="0", y="0", xunits="fraction", yunits="fraction"),
                    KML.size(x="0.4", y="0.05", xunits="fraction", yunits="fraction")
                )
            )

    f = open(global_vars.kml_destination_path + filename, "w")
    out = etree.tostring(kml, pretty_print=True).decode("utf-8")
    f.write(out)
    f.close()

def CreateLogosKML():
    kml = KML.kml(
        KML.Document(
            KML.Folder(
                KML.ScreenOverlay(
                    KML.name('Logos'),
                    KML.Icon(KML.href('http://lg1:81/SF/Logos.png')),
                    KML.overlayXY(x="0", y="1", xunits="fraction", yunits="fraction"),
                    KML.screenXY(x="0.02", y="0.9", xunits="fraction", yunits="fraction"),
                    KML.rotationXY(x="0", y="0", xunits="fraction", yunits="fraction"),
                    KML.size(x="0.5", y="0.5", xunits="fraction", yunits="fraction")
                )
            )
        )
    )
    f = open(global_vars.kml_destination_path + 'slave_{}.kml'.format(global_vars.screen_for_logos), "w")
    out = etree.tostring(kml, pretty_print=True).decode("utf-8")
    f.write(out)
    f.close()

def CreateRegionsKML(regions, date):
    kml = KML.kml(
        KML.Document(
            KML.Folder(
                KML.name('Temperature regions'))
            )
        )

    filename = global_vars.kml_destination_filename

    if date:
        filename = 'historic_' + str(date) + '.kml'
        print(filename)

    for region in regions:
        color = region.pop()
        kml.Document.Folder.append(
            KML.Placemark(
                KML.Style(
                KML.PolyStyle(
                    KML.color(color),
                    KML.outline(0)
                    )
                ),
                KML.Polygon(
                    KML.altitudeMode('absolute'),
                    KML.outerBoundaryIs(
                        KML.LinearRing(
                            KML.coordinates(GetCoords(region))
                            )
                        )
                    )
                )
            )

    f = open(global_vars.kml_destination_path + filename, "w")
    out = etree.tostring(kml, pretty_print=True).decode("utf-8")
    f.write(out)
    f.close()

def CreateKML(regions, date):
    CreateRegionsKML(regions, date)
    CreateDateAndColorbarKML(date)
    CreateLogosKML()
