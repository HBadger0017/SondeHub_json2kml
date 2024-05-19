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
with urllib.request.urlopen(url) as jsonFile:
    data = json.load(jsonFile)

# invoke simplekml
kml = simplekml.Kml()
style = simplekml.Style()
style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/pal4/icon30.png'

# array 'line' holds lon, lat, and alt varialbles from json
line = []

# Grabs the serial from the first record in json file for var title
title = data[0]['serial']

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
# Set simplekml linestring color to red; change color as desired
linestring.style.linestyle.color = simplekml.Color.red
# Set simplekml linestring width to 5 pixels; change as needed
linestring.style.linestyle.width = 5

# Points Section; additional information based on rx'd wx readings from the sonde.
for list in range(0,len(data),50):
    try:
      lon = data[list]['lon']
      lat = data[list]['lat']
      alt = data[list]['alt']
      temp = data[list]['temp']
      hum = data[list]['humidity']
      batt = data[list]['batt']
      freq = data[list]['frequency'] # tx freq of the sonde
      head = data[list]['heading'] # direction sonde is moving
      vel_h = data[list]['vel_h'] # horizontal speed of the sonde (+/-)
      vel_v = data[list]['vel_v'] # vertical speed of the sonde (+/-)

      # Creates points that correspond to the linestring above; wx data is captured and displayed
      # Makes for a long kml file and kinda klugie.
      pnt = kml.newpoint()
      pnt.snippet.content = "{0} WX Readings".format(title)
      pnt.coords = [(lon,lat,alt)]
      pnt.altitudemode = simplekml.AltitudeMode.absolute
      # Custom Description box in Google Earth.  The URI for the icon does not work properly but hope it gets fixed (may see about hosting it on my GitHub page.)
      # KML will render html for formmatting within the Description box
      pnt.description = "<b>{0}</b><br/>TX freq: {1} MHz<br/><br/>Tempurature: {2}C <br/>Humidity: {3}% <br/>Battery: {4} VDC<br/><br/>Heading: {5:.0f} Deg<br/>Horizontal Velocity: {6:.1f} m/s<br/>Vertical Velocity: {7:.1f} m/s".format(title,freq,temp,hum,batt,head,vel_h,vel_v)
      pnt.style = style

      # error handling
    except:
       continue


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