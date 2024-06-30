#####################################################################################
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
#####################################################################################
# This (v3) python script will convert the json file for a given radiosonde from sondehub.org
# and convert it to kml for plotting in Google Earth or which ever geo-type application
# used.
#
# ** UPDATE for v3 - inclusion of wx data; click on the wx/sun icon for data at that point
# Caveat:  due to the number of points captured in the data, a paired-down data set is captured
#
# Usage:
# 1) Navigate to sondehub.org
# 2) Find a radiosonde of interest (current or past [older records are gz'd and cannt be 
#    read with this script]); copy the radiosonde serial #.
# 4) Run scrpit as follows: python3 SondeHub_json2kml_v3.py <radiosonde serial #>.
# 5) A kml will be saved to the current user directory.
# 6) Open kml in Google Earth normally.
#
# NOTE: This is a visualization of radio packets recieved by the ground stations nearby
# and may not be all packets or have duplicates.  This project was to dust off my python
# on a free day I had; use at your convenience and beware of your surroundings.  Not responsible
# for any detrimental actions from using this script. 
# 
# Enjoy and modify as needed; credits at the bottom.


import json
import urllib.request
import simplekml
import sys
import codecs
from datetime import datetime
import dateutil.parser as parser

# var 'inputFile' equals the second value read by sys.argv
try:
    inputFile = sys.argv[1]
    print('Searching for radiosonde...')
# if second value is missing, print message and exit
except:
   print("Please enter a valid Radiosonde serial.")
   sys.exit(1)

# JSON Encoding is UTF-8. Change stdout to UTF-8 to prevent encoding error
# when calling print titles inside the loop
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# Change in v2 is this:  script navigates to the json directly using this url
# and the radiosonde serial
url = "https://api.v2.sondehub.org/sonde/" + inputFile
print ('Found "'+inputFile+'"')

# Opens url with serial and pulls down json data loads as var 'data'
with urllib.request.urlopen(url) as jsonFile:
  data = json.load(jsonFile)

# invoke simplekml
kml = simplekml.Kml()
style = simplekml.Style()
style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/pal4/icon30.png'

# array 'line' holds lon, lat, and alt varialbles from json
line = []
#outputFile = ''

# Grabs the serial from the first record in json file for var title
title = str(data[0]['serial'])

# Names document with var 'title'
kml.document.name = title

# for each record in var 'data', start with the first record
# put lon, lat, alt into list 'points' then skip 50 to the next record.
# Adjust range(start,data set,<count between points in data set>) for more or less linestring fidelity
for list in range(0,len(data),50):
    try:
      lon = data[list]['lon']
      lat = data[list]['lat']
      alt = data[list]['alt']
    # append array 'line' with each list of 'points'
      points = (lon,lat,alt)
      line.append(points)
    # error handling
    except:
      continue

# Create a new simplekml linestring, naming it with var 'title'
linestring = kml.newlinestring(name=title)
# put array 'line' into simplekml var 'coords'
linestring.coords = line
# Set simplekml altitude mode to be relative to ground
linestring.altitudemode = simplekml.AltitudeMode.absolute
# Extrude linestring to the ground
linestring.extrude = 1
# Set simplekml linestring color to red
linestring.style.linestyle.color = simplekml.Color.red
# Set simplekml linestring width to 10 pixels
linestring.style.linestyle.width = 5

#Points Section; additional information based on rx'd wx readings from the sonde.
for list in range(0,len(data),50):
    try:
        lon = data[list]['lon'] # longitude
        lat = data[list]['lat'] # latitude
        alt = round(data[list]['alt'], 1) # altitude
        batt = data[list]['batt'] # battery voltage
        freq = data[list]['frequency'] # tx freq of the sonde

        if 'temp' in data[list] and data[list]['temp']: # temperature
            temp = round(data[list]['temp'], 1)
        else:
            temp = "NA"

        if 'humidity' in data[list] and data[list]['humidity']: # humidity
            hum = round(data[list]['humidity'], 1)
        else:
            hum = "NA"

        if 'heading' in data[list] and data[list]['heading']: # direction of travel
            head = round(data[list]['heading'])
        else:
            head = "NA"

        if 'vel_h' in data[list] and data[list]['vel_h']: # horizontal velocity of the radiosonde (+/-)
            vel_h = round(data[list]['vel_h'], 1)
        else:
            vel_h = "NA" 

        if 'vel_v' in data[list] and data[list]['vel_v']: # vertical velocity of the radiosonde (+/-)
            vel_v = round(data[list]['vel_v'], 1)
        else:
            vel_v = "NA" 

        dt = data[list]['datetime'] # GPS time from radiosonde
        sonde_time = datetime.strftime(parser.parse(dt),'%Y-%m-%d %H:%M:%S %Z') #takes datetime and converts to more readable

        if 'manufacturer' in data[list] and data[list]['manufacturer']: # make of radioonde
            man = data[list]['manufacturer'] 
        else:
            man = "NA"
        
        if 'subtype' in data[list] and data[list]['subtype']: # model of radiosonde
            subtype = data[list]['subtype'] 
        else:
            subtype = "NA"
    except:
      continue

        # Creates points that correspond to the linestring above; wx data is captured and displayed
        # Makes for a long kml file and kinda klugie.
    pnt = kml.newpoint()
    pnt.snippet.content = "{0} WX Readings".format(title)
    pnt.coords = [(lon,lat,alt)]
    pnt.altitudemode = simplekml.AltitudeMode.absolute
        # Custom Description box in Google Earth.  The URI for the icon does not work properly but hope it gets fixed (may see about hosting it on my GitHub page.)
        # KML will render html for formmatting within the Description box
    pnt.description = "<b>{0}</b><br/><br/><u>Make: </u>{10}<br/><u>Model:</u> {11}<br/>Sonde Time:<br/>{1}<br/>TX freq: {2} MHz<br/><br/>Altitude: {6} m<br/>Heading: {7} deg<br/>Horizontal Velocity: {8} m/s<br/>Vertical Velocity: {9} m/s<br/><br/><b>WX Metrics</b><br/>Tempurature: {3}C <br/>Humidity: {4}% <br/>Battery: {5} VDC<br/>".format(title,sonde_time,freq,temp,hum,batt,alt,head,vel_h,vel_v,man,subtype)
    pnt.style = style

outputFile= (title + '.' + 'kml')
print ('Saving file "'+outputFile+'"')
kml.save(title + '.' + 'kml')

#############################################
# Credits
#
# To Patrick Eisoldt for creating the simplekml module for python
# https://pypi.org/project/simplekml/
#
# and 
#
# To d-me3 for dev'ing the json2kml script
# https://github.com/d-me3/json2kml
#
# Thanks to SondeHub.org for putting together such a great tool





# 2 spaces, not 1