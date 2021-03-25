import sys
import requests
import logging
import warnings
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth


def main(argv):
   warnings.filterwarnings("ignore")
   hostname = ''
   username = ''
   password = ''
   
   try:
      hostname = sys.argv[1]
      username = sys.argv[2]
      password = sys.argv[3]

   except:
      print('Please enter hostname/IP Address, username, and password')
      sys.exit()
	
   logging.basicConfig(filename='CUCM_SetLoad.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

   #Create a new session to maintain cookies across requests      
   s = requests.Session()
   
   headers= {"SOAPAction": "\"CUCM:DB ver=10.5 executeSQLQuery\"", "Content-Type": "text/xml"}
   update_headers = {"SOAPAction": "\"CUCM:DB ver=10.5 executeSQLUpdate\"", "Content-Type": "text/xml"}

   device_query = '<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:ns=\"http://www.cisco.com/AXL/API/10.5\"><soapenv:Body><ns:executeSQLQuery><sql>select name as devicename,pkid,tkmodel from device where specialloadinformation = \'\'</sql></ns:executeSQLQuery></SOAP-ENV:Envelope>'
   device_query_xml = s.post('https://' + hostname + ':8443/axl/', verify=False, auth=HTTPBasicAuth(username,password),headers=headers, data=device_query)
   device_soup = BeautifulSoup(device_query_xml.text)
   device_list = device_soup.find_all('row')
   device_defaults_query = '<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:ns=\"http://www.cisco.com/AXL/API/10.5\"><soapenv:Body><ns:executeSQLQuery><sql>select tkmodel,loadinformation from defaults where loadinformation &lt;&gt; \'\'</sql></ns:executeSQLQuery></SOAP-ENV:Envelope>'
   device_defaults_query_xml = s.post('https://' + hostname + ':8443/axl/', verify=False, headers=headers, data=device_defaults_query)
   device_defaults_soup = BeautifulSoup(device_defaults_query_xml.text)
   device_defaults_list = device_defaults_soup.find_all('row')
   device_defaults_dict = {}
   for row in device_defaults_list:
      device_defaults_dict[row.tkmodel.get_text()] = row.loadinformation.get_text()
   for row in device_list:
      try:
          update_device_query = '<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:ns=\"http://www.cisco.com/AXL/API/10.5\"><soapenv:Body><ns:executeSQLUpdate><sql>update device set specialloadinformation = \''+device_defaults_dict[row.tkmodel.get_text()]+'\' where pkid = \''+row.pkid.get_text()+'\'</sql></ns:executeSQLUpdate></SOAP-ENV:Envelope>'
          update_device_xml = s.post('https://' + hostname + ':8443/axl/', verify=False,headers=update_headers, data=update_device_query)
          logging.debug('successfully updated device: ' + row.devicename.get_text() + ',' + device_defaults_dict[row.tkmodel.get_text()])
      except:
          logging.debug('could not update device: ' + row.devicename.get_text())

if __name__ == "__main__":
   #Replace the below values or pass the commands through the command-line and remove the below line
   sys.argv = ["CUCM_SetLoad.py", "192.168.1.1","ccmadministrator", "password123"]
   main(sys.argv[1:])

