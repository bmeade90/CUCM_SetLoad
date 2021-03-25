# CUCM_SetLoad

This program will hard set the device load for every phone that doesn't have it set already based on the Device Defaults.  This can be used for CUCM cluster upgrades where you need to make sure phones do not upgrade firmware.

PIP Packages needed:

requests (py.exe -m pip install requests)

BeautifulSoup4 (py.exe -m pip install BeautifulSoup4)

Then run the program C:>py.exe CUCM_SetLoad.py hostname/IP username password
