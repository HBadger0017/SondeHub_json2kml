#####################################################################################
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
#####################################################################################
# This (v2) python script will convert the json file for a given radiosonde from sondehub.org
# and convert it to kml for plotting in Google Earth or which ever geo-type application
# used.
#
# Usage:
# 1) Navigate to sondehub.org
# 2) Find a radiosonde of interest (current or past); copy radiosonde serial
# 4) Run scrpit as follows: SondeHub_json2kml_v2.py <radiosonde serial>
# 5) A kml will be saved to the current user directory
# 6) Open kml in Google Earth
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
import os

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
with urllib.request.urlopen(url) as jsonData:
    data = json.load(jsonData)

kml = simplekml.Kml()
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
# Set simplekml linestring color to red; change color as desired
linestring.style.linestyle.color = simplekml.Color.red
# Set simplekml linestring width to 5 pixels; change as needed
linestring.style.linestyle.width = 5

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





# 2 spaces, not 1