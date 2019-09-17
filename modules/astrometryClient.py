import requests
import json
from urllib.request import Request, urlopen
from ftplib import FTP
import os
import fileinput
import time
from PIL import Image


#Global variables
astrometrySessionKey = None

#Uses ftp
def upload_file(path):
    ftp = FTP()
    ftp.set_debuglevel(2)
    ftp.connect('ftp.cluster023.hosting.ovh.net', 21)
    ftp.login('simulacioh-perseidas','Marruecos2019') #Using mydomotik server, please change
    try:
        ftp.delete('frame.jpg')
    except:
        print('')
    fp = open(path, 'rb')
    ftp.storbinary('STOR %s' % 'frame.jpg', fp, 1024)
    fp.close()
    return 'https://www.mydomotik.com/PerseidasPy/frame.jpg' #Change this link too


#Connects to nova.astrometry.net API
def AstrometryNetConnect():
    AstrometryRequest = requests.post('http://nova.astrometry.net/api/login', data={'request-json': json.dumps({"apikey": "pamhwodavppqtdyg"})})
    response = json.loads(AstrometryRequest.text)
    global astrometrySessionKey
    astrometrySessionKey = response['session']

    if response['status'] == "success":
        print('Logged In to Astrometry.net')
        return astrometrySessionKey
    else:
        print('ERROR')
        print(response)
        exit()


#Requests astrometry data from URL image
def AstrometryNetRequest(path):
    im=Image.open(path)
    img_width, img_height = im.size
    Cx, Cy = img_width/2, img_height/2
    print('Starting nova.astrometry.net request')
    url = upload_file(path)
    print('Uploaded')
    AstrometryRequest = requests.post('http://nova.astrometry.net/api/url_upload', data={'request-json': json.dumps({"session": astrometrySessionKey, "url": "http://mydomotik.com/PerseidasPy/frame.jpg"})})
    response = json.loads(AstrometryRequest.text)
    subid = response['subid']

    processStatus = False

    while processStatus == False:
        time.sleep(10)
        print('Waiting for jobs...')
        AstrometryRequest = requests.post('http://nova.astrometry.net/api/submissions/'+str(subid))
        response = json.loads(AstrometryRequest.text)

        if len(response['jobs']) != 0 and response['jobs'][0] != None:
            processStatus = True
            jobid = response['jobs'][0]
            jobStatus = False

    while jobStatus == False:
        AstrometryRequest = requests.post('http://nova.astrometry.net/api/jobs/'+str(jobid))
        response = json.loads(AstrometryRequest.text)

        if response['status'] == 'success':
            jobStatus = True
            AstrometryRequest = requests.post('http://nova.astrometry.net/api/jobs/'+str(jobid)+'/calibration/')
            response = json.loads(AstrometryRequest.text)
            response['Cx'] = Cx
            response['Cy'] = Cy
            return response

#Init script
AstrometryNetConnect()
