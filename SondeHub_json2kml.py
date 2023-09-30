#####################################################################################
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
#####################################################################################
# This python script will convert the json file for a given radiosonde from sondehub.org
# and convert it to kml for plotting in Google Earth or which ever geo-type application
# used.
#
# Usage:
# 1) Navigate to sondehub.org
# 2) Find/click a radiosonde of interest (current or past)
# 3) On the left hand side of the screen, Click "Plots" to open Grafana for that radiosonde
# 4) in Grafana, scroll down to "Export Data for current Time Range" (NOTE: adjust timeframe
# at the top of Grafana to match radiosonde launch time; does not have to be exact
# 5) Click "Download json" or right-click to 'open in new tab'
# 6) Copy json code that appears
# 7) Save as <sonde name>.json in text/code editor of choice
# 
# 8) run scrpit as follows: SondeHub_json2kml.py </path/to/file.json>
# 9) A kml will be saved to the current user directory
# 10) Open kml in Google Earth
#
# NOTE: This is a visualization of radio packets recieved by the ground stations nearby
# and may not be all packets or have duplicates.  This project was to dust off my python
# on a free day I had; use at your convenience and beware of your surroundings.  Not responsible
# for any detrimental actions from using this script. 
# 
# Enjoy and modify as needed; credits at the bottom.
   
import os
import json
import simplekml
import sys
import codecs

# var 'inputFile' equals the second value read by sys.argv
try:
    inputFile = sys.argv[1]
# if second value is missing, print message and exit
except:
    print("Please enter a valid /path/to/file.json")
    sys.exit(1)

# JSON Encoding is UTF-8. Change stdout to UTF-8 to prevent encoding error
# when calling print titles inside the loop
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

print ('Opening file "'+inputFile+'"')

# Opens json file and loads as var 'data'
with open (inputFile) as jsonFile:
    data = json.load(jsonFile)
    
kml = simplekml.Kml ()
# array 'line' holds lon, lat, and alt varialbles from json
line = []
# Grabs the serial from the first record in json file for var title
title = data[0]['serial']

# Names document with var 'title'
kml.document.name = title

# for each record in var 'data', start with the first record
# put lon, lat, alt into list 'points' then skip 50 to the next record.
# Adjust this rate for more or less linestring fidelity
for list in range(0,len(data),50):
    lon = data[list]['lon']
    lat = data[list]['lat']
    alt = data[list]['alt']
    # append array 'line' with each list of 'points'
    points = (lon,lat,alt)
    line.append(points)

# Create a new simplekml linestring, naming it with var 'title'
linestring = kml.newlinestring(name=title)
# put array 'line' into simplekml var 'coords'
linestring.coords = line
# Set simplekml altitude mode to be relative to ground
linestring.altitudemode = simplekml.AltitudeMode.relativetoground
# Extrude linestring to the ground
linestring.extrude = 1
# Set simplekml linestring color to red
linestring.style.linestyle.color = simplekml.Color.red
# Set simplekml linestring width to 10 pixels
linestring.style.linestyle.width = 10
        
outputFile = (title + '.' + 'kml')
print ('Saving file "'+outputFile+'"')
kml.save (title + '.' + 'kml')
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