import xml.etree.ElementTree as ET
import sys
from testrail import *

class UFT:

    def __init__(self, xml):
        self.XML = xml
        self.testname = ""
        self.status = ""
        
    def updateResult(self, result):
        if result == 'Passed':
            self.status = '1' 
        elif result == 'Failed':
            self.status = '5'
        elif result == 'Stopped':
            self.status = '2'
        else:
            print ("Unknown status, exiting!")
            sys.exit(2)

    def getTestName(self):
        print ("Getting Test Name")
        tree = ET.parse(self.XML)
        for element in tree.findall('.//DName'):
            self.testname = element.text

    def processResult(self):
        print ("Getting Result of test")
        tree = ET.parse(self.XML)
        for element in tree.findall('.//NodeArgs'):
            if element.attrib['eType'] == 'StartIteration':
                self.updateResult(element.attrib['status'])

    def updateTestRail(self, URL):
        print ("Connecting to Test Rail")
        tr = APIClient(URL)
        tr.user = 'andygmo@gmail.com'
        tr.password = 'testpass123'
        print ("Posting Results")
        tr.send_post('add_result/1', {'status_id':self.status})


uft = UFT("Results.xml")
uft.getTestName()
uft.processResult()
uft.updateTestRail('https://andygmo.testrail.io/')
