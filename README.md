# SondeHub_json2kml_v2
## Script to convert radiosonde json from sondehub.org into kml

This (v2) python3 script will convert the json file for a given radiosonde from sondehub.org and convert it to kml for plotting in Google Earth or which ever geo-type application used.

### Usage:
1) Navigate to sondehub.org
2) Find a radiosonde of interest (current or past); copy radiosonde serial
    #### Format
    U or V#######
    #### Example
    V1620896

3) Run scrpit as follows:
```
SondeHub_json2kml_v2.py <radiosonde serial>
```
4) A kml will be saved to the current user directory
5) Open kml in Google Earth

**NOTE**: This is a visualization of radio packets recieved by the ground stations from a radiosonde and may not be all packets or have duplicates.  I had a free day and decided to dust off my python; use at your convenience and beware of your surroundings. 

**_I am not responsible for any detrimental actions from using this script!_**

Enjoy and modify as needed.

### Credits
To Patrick Eisoldt for creating the simplekml module for python (https://pypi.org/project/simplekml)

and

To d-me3 for dev'ing the json2kml script (https://github.com/d-me3/json2kml)

Finally,

Thanks to SondeHub.org for putting together such a great tool.
