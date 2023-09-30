# SondeHub_json2kml
## Script to convert radiosonde json from sondehub.org into kml

This python3 script will convert json data for a given radiosonde, pulled from sondehub.org, and convert the json to kml for plotting in Google Earth (or which ever geo-type application used).

### Usage:
1) Navigate to sondehub.org
2) Find/click a radiosonde of interest (current or past)
3) On the left hand side of the screen, Click "Plots" to open Grafana for that radiosonde
4) in Grafana, scroll down to "Export Data for current Time Range" (NOTE: adjust timeframe
at the top of Grafana to match radiosonde launch time; does not have to be exact
5) Click "Download json" or right-click to 'open in new tab'
6) Copy json code that appears
7) Save as <sonde name>.json in text/code editor of choice
8) Run script as follows:
```
python3 SondeHub_json2kml.py </path/to/file>.json
```
10) A kml will be saved to the current user directory
11) Open kml in Google Earth

**NOTE**: This is a visualization of radio packets recieved by the ground stations from a radiosonde and may not be all packets or have duplicates.  I had a free day and decided to dust off my python; use at your convenience and beware of your surroundings. 

**_I am not responsible for any detrimental actions from using this script!_**

Enjoy and modify as needed.

### Credits
To Patrick Eisoldt for creating the simplekml module for python (https://pypi.org/project/simplekml)

and

To d-me3 for dev'ing the json2kml script (https://github.com/d-me3/json2kml)

Finally,

Thanks to SondeHub.org for putting together such a great tool.
